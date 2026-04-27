from __future__ import annotations

import csv
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None


BASE_URL = "https://lod.lu/api/lb"
INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("outputs")
AUDIO_DIR = Path("audios")
OUTPUT_HEADERS = [
    "luxemburgues",
    "portugues",
    "ingles",
    "link audio 1",
    "link audio 2",
]
DEFAULT_EMPTY_ROW = {
    "luxemburgues": "",
    "portugues": "",
    "ingles": "",
    "link audio 1": "",
    "link audio 2": "",
}


def ensure_directories() -> None:
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    AUDIO_DIR.mkdir(exist_ok=True)


def request_url(url: str) -> Any:
    request = Request(
        url,
        headers={
            "User-Agent": "FlashcardMaker/1.0",
            "Accept": "*/*",
        },
    )
    return urlopen(request, timeout=30)


def get_json(url: str) -> Any:
    with request_url(url) as response:
        return json.load(response)


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or "sem_nome"


def build_search_url(word: str) -> str:
    params = urlencode({"lang": "lb", "query": word})
    return f"{BASE_URL}/search?{params}"


def build_entry_url(article_id: str) -> str:
    return f"{BASE_URL}/entry/{quote(article_id)}"


def choose_result(word: str, results: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not results:
        return None

    exact_case = [item for item in results if item.get("word_lb") == word]
    if exact_case:
        return exact_case[0]

    lower_word = word.casefold()
    exact_fold = [item for item in results if str(item.get("word_lb", "")).casefold() == lower_word]
    if exact_fold:
        return exact_fold[0]

    return results[0]


def flatten_translations(entry_data: dict[str, Any], lang: str) -> str:
    values: list[str] = []
    seen: set[str] = set()

    entry = entry_data.get("entry", {})
    for micro in entry.get("microStructures", []):
        for unit in micro.get("grammaticalUnits", []):
            for meaning in unit.get("meanings", []):
                target = meaning.get("targetLanguages", {}).get(lang, {})
                for part in target.get("parts", []):
                    if part.get("type") != "translation":
                        continue
                    content = str(part.get("content", "")).strip()
                    if not content:
                        continue
                    key = content.casefold()
                    if key in seen:
                        continue
                    seen.add(key)
                    values.append(content)

    return "; ".join(values)


def download_audio(audio_url: str, article_id: str, word: str) -> None:
    if not audio_url:
        return

    parsed = urlparse(audio_url)
    suffix = Path(parsed.path).suffix or ".ogg"
    filename = f"{sanitize_filename(word)}__{sanitize_filename(article_id)}{suffix}"
    destination = AUDIO_DIR / filename
    if destination.exists():
        return

    with request_url(audio_url) as response, destination.open("wb") as handle:
        handle.write(response.read())


def fetch_word_data(word: str) -> dict[str, str]:
    search_data = get_json(build_search_url(word))
    result = choose_result(word, search_data.get("results", []))
    if not result:
        empty_row = dict(DEFAULT_EMPTY_ROW)
        empty_row["luxemburgues"] = word
        return empty_row

    article_id = str(result["article_id"])
    entry_data = get_json(build_entry_url(article_id))
    audio_files = entry_data.get("entry", {}).get("audioFiles", {}) or {}
    audio_1 = str(audio_files.get("ogg", ""))
    audio_2 = str(audio_files.get("aac", ""))

    if audio_1:
        download_audio(audio_1, article_id, word)

    return {
        "luxemburgues": word,
        "portugues": flatten_translations(entry_data, "pt"),
        "ingles": flatten_translations(entry_data, "en"),
        "link audio 1": audio_1,
        "link audio 2": audio_2,
    }


def read_words(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV sem cabecalho: {path.name}")
        source_column = reader.fieldnames[0]
        return [str(row.get(source_column, "")).strip() for row in reader if str(row.get(source_column, "")).strip()]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def iter_csv_inputs() -> list[Path]:
    return sorted(path for path in INPUT_DIR.glob("*.csv") if path.is_file())


def create_progress(iterable: list[Any], desc: str, unit: str) -> Any:
    if tqdm is None:
        return iterable
    return tqdm(iterable, desc=desc, unit=unit)


def process_csv(input_path: Path, cache: dict[str, dict[str, str]]) -> None:
    output_path = OUTPUT_DIR / input_path.name
    if output_path.exists():
        print(f"Pulando {input_path.name}: ja existe em outputs.")
        return

    words = read_words(input_path)
    rows: list[dict[str, str]] = []
    word_iterable = create_progress(words, f"Palavras {input_path.name}", "palavra")

    for index, word in enumerate(word_iterable, start=1):
        if word not in cache:
            try:
                cache[word] = fetch_word_data(word)
            except (HTTPError, URLError, TimeoutError) as exc:
                print(f"[{input_path.name} {index}/{len(words)}] Falha em '{word}': {exc}", file=sys.stderr)
                empty_row = dict(DEFAULT_EMPTY_ROW)
                empty_row["luxemburgues"] = word
                cache[word] = empty_row
            time.sleep(0.05)

        rows.append(dict(cache[word]))
        if tqdm is None:
            print(f"[{input_path.name} {index}/{len(words)}] {word}")

    write_rows(output_path, rows)
    print(f"Gerado: {output_path}")


def main() -> int:
    ensure_directories()
    cache: dict[str, dict[str, str]] = {}
    input_files = iter_csv_inputs()

    if not input_files:
        print("Nenhum CSV encontrado em inputs.")
        return 0

    file_iterable = create_progress(input_files, "Arquivos", "arquivo")
    for input_path in file_iterable:
        process_csv(input_path, cache)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
