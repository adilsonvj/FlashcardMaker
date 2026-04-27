from __future__ import annotations

import csv
import os
import html
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse


OUTPUTS_DIR = Path("outputs")
AUDIO_SOURCE_DIR = Path("audios")
IMPORT_FILES = {
    "pt": Path("anki_flashcards_import.csv"),
    "en": Path("anki_flashcards_import_en.csv"),
}
MANUAL_REVIEW_FILES = {
    "pt": Path("anki_flashcards_manual_review.csv"),
    "en": Path("anki_flashcards_manual_review_en.csv"),
}
MANUAL_REVIEW_HEADERS = [
    "luxemburgues",
    "portugues",
    "ingles",
    "link audio 1",
    "link audio 2",
    "motivo",
    "arquivo_origem",
]
LANGUAGE_SOURCE_FIELD = {
    "pt": "portugues",
    "en": "ingles",
}
LANGUAGE_REASON = {
    "pt": "sem_traducao_portugues",
    "en": "sem_traducao_ingles",
}


def resolve_anki_media_dir() -> Path:
    configured = os.environ.get("ANKI_MEDIA_DIR", "").strip()
    if configured:
        return Path(configured)

    appdata = os.environ.get("APPDATA", "").strip()
    if not appdata:
        raise RuntimeError(
            "Nao foi possivel localizar a pasta do Anki automaticamente. "
            "Defina a variavel de ambiente ANKI_MEDIA_DIR."
        )

    anki_base = Path(appdata) / "Anki2"
    if not anki_base.exists():
        raise RuntimeError(
            "A pasta base do Anki nao foi encontrada. "
            "Defina a variavel de ambiente ANKI_MEDIA_DIR."
        )

    profile_dirs = sorted(
        path for path in anki_base.iterdir() if path.is_dir() and (path / "collection.media").exists()
    )
    if len(profile_dirs) == 1:
        return profile_dirs[0] / "collection.media"

    raise RuntimeError(
        "Nao foi possivel escolher automaticamente a pasta collection.media do Anki. "
        "Defina a variavel de ambiente ANKI_MEDIA_DIR com o caminho correto."
    )


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or "sem_nome"


def first_translation(value: str) -> str:
    if not value:
        return ""
    return value.split(";")[0].strip()


def derive_audio_filename(word: str, audio_url: str) -> str:
    parsed = urlparse(audio_url)
    stem = Path(parsed.path).stem
    suffix = Path(parsed.path).suffix or ".ogg"
    article_id = stem.upper()
    return f"{sanitize_filename(word)}__{sanitize_filename(article_id)}{suffix}"


def resolve_audio_file(word: str, audio_url: str) -> Path | None:
    if not audio_url:
        return None

    exact_name = derive_audio_filename(word, audio_url)
    exact_path = AUDIO_SOURCE_DIR / exact_name
    if exact_path.exists():
        return exact_path

    prefix = f"{sanitize_filename(word)}__"
    candidates = sorted(AUDIO_SOURCE_DIR.glob(f"{prefix}*.ogg"))
    if candidates:
        return candidates[0]

    return None


def card_one_front(audio_filename: str) -> str:
    return (
        '<div style="font-family:Arial,sans-serif;font-size:30px;line-height:1.2;'
        'text-align:center;">'
        f'[sound:{html.escape(audio_filename)}]'
        "</div>"
    )


def card_one_back(word: str, translation: str) -> str:
    return (
        '<div style="font-family:Arial,sans-serif;text-align:center;">'
        f'<div style="font-size:34px;font-weight:700;line-height:1.2;">{html.escape(word)}</div>'
        f'<div style="font-size:24px;line-height:1.4;margin-top:8px;">({html.escape(translation)})</div>'
        "</div>"
    )


def card_two_front(translation: str) -> str:
    return (
        '<div style="font-family:Arial,sans-serif;text-align:center;'
        'font-size:32px;font-weight:700;line-height:1.2;">'
        f'{html.escape(translation)}'
        "</div>"
    )


def card_two_back(word: str, audio_filename: str) -> str:
    return (
        '<div style="font-family:Arial,sans-serif;text-align:center;">'
        f'<div style="font-size:34px;font-weight:700;line-height:1.2;">{html.escape(word)}</div>'
        f'<div style="font-size:30px;line-height:1.2;margin-top:12px;">[sound:{html.escape(audio_filename)}]</div>'
        "</div>"
    )


def collect_rows(language: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    valid_rows: list[dict[str, str]] = []
    review_rows: list[dict[str, str]] = []
    seen_words: set[str] = set()
    translation_field = LANGUAGE_SOURCE_FIELD[language]
    missing_translation_reason = LANGUAGE_REASON[language]

    for csv_path in sorted(OUTPUTS_DIR.glob("*.csv")):
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                word = (row.get("luxemburgues") or "").strip()
                if not word:
                    continue

                key = word.casefold()
                if key in seen_words:
                    continue
                seen_words.add(key)

                portuguese_full = (row.get("portugues") or "").strip()
                english_full = (row.get("ingles") or "").strip()
                translation_full = (row.get(translation_field) or "").strip()
                audio_link_1 = (row.get("link audio 1") or "").strip()
                audio_link_2 = (row.get("link audio 2") or "").strip()
                translation = first_translation(translation_full)
                audio_path = resolve_audio_file(word, audio_link_1)

                reasons: list[str] = []
                if not translation:
                    reasons.append(missing_translation_reason)
                if not audio_link_1:
                    reasons.append("sem_link_audio_1")
                elif audio_path is None:
                    reasons.append("audio_nao_encontrado_na_pasta_audios")

                if reasons:
                    review_rows.append(
                        {
                            "luxemburgues": word,
                            "portugues": portuguese_full,
                            "ingles": english_full,
                            "link audio 1": audio_link_1,
                            "link audio 2": audio_link_2,
                            "motivo": "; ".join(reasons),
                            "arquivo_origem": csv_path.name,
                        }
                    )
                    continue

                valid_rows.append(
                    {
                        "luxemburgues": word,
                        "translation": translation,
                        "audio_filename": audio_path.name,
                        "audio_path": str(audio_path),
                    }
                )

    return valid_rows, review_rows


def copy_audio_to_anki_media(rows: list[dict[str, str]], anki_media_dir: Path) -> None:
    anki_media_dir.mkdir(parents=True, exist_ok=True)

    for row in rows:
        source = Path(row["audio_path"])
        destination = anki_media_dir / row["audio_filename"]
        if destination.exists():
            continue
        shutil.copy2(source, destination)


def write_import_csv(rows: list[dict[str, str]], destination: Path) -> None:
    with destination.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)

        for row in rows:
            word = row["luxemburgues"]
            translation = row["translation"]
            audio_filename = row["audio_filename"]

            writer.writerow([card_one_front(audio_filename), card_one_back(word, translation)])
            writer.writerow([card_two_front(translation), card_two_back(word, audio_filename)])


def write_manual_review_csv(rows: list[dict[str, str]], destination: Path) -> None:
    with destination.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANUAL_REVIEW_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def build_language_export(language: str, anki_media_dir: Path) -> None:
    valid_rows, review_rows = collect_rows(language)
    copy_audio_to_anki_media(valid_rows, anki_media_dir)
    write_import_csv(valid_rows, IMPORT_FILES[language])
    write_manual_review_csv(review_rows, MANUAL_REVIEW_FILES[language])
    print(f"[{language}] Cards unicos: {len(valid_rows)}")
    print(f"[{language}] Pendencias para revisao manual: {len(review_rows)}")
    print(f"[{language}] Arquivo gerado: {IMPORT_FILES[language]}")
    print(f"[{language}] Arquivo de revisao: {MANUAL_REVIEW_FILES[language]}")


def main() -> int:
    anki_media_dir = resolve_anki_media_dir()
    print(f"Pasta de midia do Anki: {anki_media_dir}")
    build_language_export("pt", anki_media_dir)
    build_language_export("en", anki_media_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
