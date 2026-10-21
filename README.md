# File Organizer CLI

[![tests](https://github.com/pythoncoderc-rgb/python-file-organizer/actions/workflows/tests.yml/badge.svg)](https://github.com/pythoncoderc-rgb/python-file-organizer/actions/workflows/tests.yml)

A small Python utility that groups top-level files into category folders based on extension.

The command is **dry-run by default**: it prints the complete plan without moving anything. File changes only happen when `--apply` is explicitly supplied.

## Why this project

This project demonstrates practical filesystem automation with a safety-first interface rather than a large dependency stack.

## Features

- Dry-run by default
- Explicit `--apply` mode
- Categories for images, documents, spreadsheets, archives, audio, video, code, and other files
- Case-insensitive extension matching
- Collision-safe destination names (`notes.txt` → `notes_1.txt`)
- Dotfiles skipped by default
- Unit tests built entirely on the Python standard library
- GitHub Actions on Windows and Linux
- No runtime third-party dependencies

## Install for development

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
```

## Preview a plan

```bash
file-organizer C:\\Users\\me\\Downloads
```

Example:

```text
DRY RUN: 3 file(s)
  photo.png -> Images/photo.png
  report.pdf -> Documents/report.pdf
  script.py -> Code/script.py
No files were changed. Run again with --apply to perform the moves.
```

## Apply the plan

```bash
file-organizer C:\\Users\\me\\Downloads --apply
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Safety notes

- Only top-level files are considered; directories are not recursively rearranged.
- Hidden dotfiles are ignored unless `--include-hidden` is used.
- Existing filenames are never overwritten; a numeric suffix is chosen instead.
- Review dry-run output before using `--apply` on important folders.

## License

MIT
