# FlashcardMaker

FlashcardMaker is a small Python workflow for turning Luxembourgish vocabulary lists into Anki-ready flashcards with audio.

It does three main things:

1. reads raw CSV word lists from `inputs/`
2. enriches them with Portuguese and English translations from `lod.lu`
3. generates Anki import files and copies the required audio into Anki's media folder

This project is useful if you are studying Luxembourgish and want a repeatable way to build listening and vocabulary cards from your own lesson lists.

## Features

- Enriches Luxembourgish word lists through the `lod.lu` API
- Downloads word audio files
- Builds deduplicated Anki flashcards in Portuguese
- Builds deduplicated Anki flashcards in English
- Separates incomplete entries into manual review CSV files
- Copies the required audio files into Anki's `collection.media` folder

## Repository structure

- `enrich_lod_csv.py`
  - reads raw input CSV files from `inputs/`
  - creates enriched CSV files in `outputs/`
  - downloads source audio into `audios/`

- `generate_anki_cards.py`
  - reads enriched CSV files from `outputs/`
  - creates Anki import CSV files in the project root
  - converts local audio to MP3 for Anki cards
  - copies the needed audio files into Anki's media folder

- `project_context/`
  - internal project documentation
  - workflow notes
  - implementation decisions
  - Anki import guidance

Ignored/generated folders:

- `inputs/`
- `outputs/`
- `audios/`
- generated Anki CSV files

These are intentionally excluded from Git by `.gitignore`.

## Requirements

- Python 3.12 or newer recommended
- Internet access for `lod.lu`
- `tqdm` installed if you want progress bars
- Anki Desktop if you want to import cards and use audio properly

Optional:

- Anki on mobile
  - AnkiDroid on Android
  - AnkiMobile on iPhone/iPad

## Optional environment variable

You can define `ANKI_MEDIA_DIR` if the script cannot automatically find your Anki media folder.

Example on Windows PowerShell:

```powershell
$env:ANKI_MEDIA_DIR="C:\Users\<YOUR_USER>\AppData\Roaming\Anki2\<YOUR_PROFILE>\collection.media"
```

There is also a sample file in:

- `.env.example`

## Input format

Put raw CSV files into `inputs/`.

The script expects:

- a CSV file
- a header row
- the first column containing the Luxembourgish words

Example:

```csv
lektioun
iech
virstellen
verb
```

## Step 1: Enrich the vocabulary lists

Run:

```powershell
python enrich_lod_csv.py
```

What it does:

- scans `inputs/` for CSV files
- skips any file that already exists in `outputs/`
- queries `lod.lu`
- writes enriched CSV files into `outputs/`
- downloads source audio files into `audios/`

The output CSV columns are:

- `luxemburgues`
- `portugues`
- `ingles`
- `link audio 1`
- `link audio 2`

## Step 2: Generate the Anki import files

Run:

```powershell
python generate_anki_cards.py
```

What it does:

- reads all enriched CSV files from `outputs/`
- keeps only unique Luxembourgish words across files
- uses only the first Portuguese translation
- uses only the first English translation
- excludes entries with missing translation or missing audio
- copies the needed audio files into Anki's media folder
- creates import files for Anki

Files generated:

- `anki_flashcards_import.csv`
- `anki_flashcards_import_en.csv`
- `anki_flashcards_manual_review.csv`
- `anki_flashcards_manual_review_en.csv`

## Flashcard format

### Portuguese deck

Card type 1:

- front: Luxembourgish word and audio
- back: first Portuguese translation only

Card type 2:

- front: first Portuguese translation only
- back: Luxembourgish word and audio

### English deck

Card type 1:

- front: Luxembourgish word and audio
- back: first English translation only

Card type 2:

- front: first English translation only
- back: Luxembourgish word and audio

## Manual review files

Not every word has a usable translation or audio.

Those entries are not turned into cards. Instead, they are collected into:

- `anki_flashcards_manual_review.csv`
- `anki_flashcards_manual_review_en.csv`

These files help you review and fix incomplete entries manually before generating more cards later.

## Anki guide for complete beginners

If you have never used Anki before, this is the simplest path.

### 1. Install Anki on your computer

Go to the official Anki website and download Anki Desktop for your operating system.

After installing it:

1. open Anki
2. create a profile if Anki asks for one
3. open the main window once so Anki creates its folders

Important:

- desktop Anki is the best place to do the initial import
- audio handling is easiest on desktop

### 2. Install Anki on your phone

Use one of these:

- Android: AnkiDroid
- iPhone/iPad: AnkiMobile

The easiest workflow is:

1. import everything on desktop first
2. create or log in to your AnkiWeb account
3. sync desktop Anki
4. log in on your phone
5. sync on the phone

This is better than trying to manually move files to the phone.

## How to find Anki's media folder

Anki stores audio, images, and other media in a folder called `collection.media`.

Typical Windows location:

```text
C:\Users\<YOUR_USER>\AppData\Roaming\Anki2\<YOUR_PROFILE>\collection.media
```

### Safest manual method

1. open Anki Desktop
2. open your profile
3. locate the profile folder from Anki or from the path above
4. enter `collection.media`

### Automatic method used by this project

`generate_anki_cards.py` tries this order:

1. use `ANKI_MEDIA_DIR` if you defined it
2. otherwise scan `%APPDATA%\Anki2`
3. if exactly one profile with `collection.media` exists, use it automatically
4. if there is ambiguity, ask you to define `ANKI_MEDIA_DIR`

## What audio files need to be moved

If `generate_anki_cards.py` runs successfully, it already copies the needed audio files into Anki's media folder.

So in the normal workflow, you do not need to move audio files by hand.

If you ever want to do it manually:

1. open `audios/`
2. copy the `.mp3` files
3. paste them into Anki's `collection.media` folder

## How to import the cards into Anki Desktop

### Portuguese deck

Import:

- `anki_flashcards_import.csv`

### English deck

Import:

- `anki_flashcards_import_en.csv`

### Import steps

1. open Anki Desktop
2. create a new deck or choose an existing one
3. click `Import`
4. choose the CSV file
5. select the target deck
6. choose or create a note type with 2 fields
7. map:
   - column 1 -> front field
   - column 2 -> back field
8. confirm import

## Recommended note type

A simple 2-field note type is enough.

Suggested field names:

- `Front`
- `Back`

Suggested note type names:

- `Luxembourgish Audio PT`
- `Luxembourgish Audio EN`

## Suggested Anki deck setup for better learning

If you add too many new cards at once, reviews can become overwhelming. Start a bit conservatively.

### New cards per day

Recommended starting point:

- `10` to `20`

If you are comfortable:

- `25`

If reviews feel heavy:

- `5` to `10`

### Maximum reviews per day

Recommended:

- `9999`

Reason:

- it is usually better not to artificially block review cards

### Learning steps

Good starting options:

- `1m 10m 1d`

Or a lighter option:

- `10m 1d`

### Graduating interval

Recommended:

- `3 days`

### Easy interval

Recommended:

- `5` to `7 days`

### Relearning step for lapses

Recommended:

- `10m`

### Leech threshold

Recommended:

- `8`

This helps flag difficult cards that keep failing.

## Recommended study strategy

For vocabulary, this works well:

1. study every day, even if only a little
2. keep daily new cards low at first
3. listen before flipping the card
4. say the Luxembourgish word out loud
5. on translation cards, try to recall pronunciation before revealing the answer

## Suggested order for new learners

If you are new to the language, a good progression is:

1. import the Portuguese deck first
2. study it for a few days
3. import the English deck later if you also want that direction

This keeps review pressure under control.

## Recommended workflow summary

1. put raw CSV files into `inputs/`
2. run `python enrich_lod_csv.py`
3. run `python generate_anki_cards.py`
4. open Anki Desktop
5. import `anki_flashcards_import.csv` and/or `anki_flashcards_import_en.csv`
6. sync to AnkiWeb
7. sync your phone

## Before publishing or sharing this repository

This repository is configured so that generated data stays out of Git.

Still, before pushing changes:

1. check `git status`
2. confirm that `inputs/`, `outputs/`, `audios/`, and generated CSV files are ignored
3. make sure you did not add local secrets or personal paths

## Useful project files

- `project_context/workflow.md`
- `project_context/decisions.md`
- `project_context/anki_generation.md`
- `project_context/anki_import_guide.md`

## License

No license file has been added yet.
