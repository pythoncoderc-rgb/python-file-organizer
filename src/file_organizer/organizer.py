from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


CATEGORY_EXTENSIONS: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"},
    "Documents": {".pdf", ".txt", ".md", ".doc", ".docx", ".odt", ".rtf"},
    "Spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "Archives": {".zip", ".7z", ".rar", ".tar", ".gz"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Code": {".py", ".cpp", ".c", ".h", ".hpp", ".js", ".ts", ".json", ".toml", ".yaml", ".yml"},
}


@dataclass(frozen=True)
class MoveOperation:
    source: Path
    destination: Path
    category: str


def classify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if suffix in extensions:
            return category
    return "Other"


def _unique_destination(destination: Path, reserved: set[Path]) -> Path:
    if not destination.exists() and destination not in reserved:
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists() and candidate not in reserved:
            return candidate
        counter += 1


def build_plan(directory: Path, *, include_hidden: bool = False) -> list[MoveOperation]:
    """Build a non-destructive organization plan for top-level files."""
    directory = directory.expanduser().resolve()
    if not directory.exists():
        raise FileNotFoundError(directory)
    if not directory.is_dir():
        raise NotADirectoryError(directory)

    plan: list[MoveOperation] = []
    reserved: set[Path] = set()

    for path in sorted(directory.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_file():
            continue
        if not include_hidden and path.name.startswith("."):
            continue

        category = classify_file(path)
        target_dir = directory / category
        destination = _unique_destination(target_dir / path.name, reserved)
        reserved.add(destination)
        plan.append(MoveOperation(path, destination, category))

    return plan


def apply_plan(plan: list[MoveOperation]) -> int:
    """Apply a previously built move plan and return the number of moved files."""
    moved = 0
    for operation in plan:
        if not operation.source.exists():
            raise FileNotFoundError(operation.source)
        operation.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(operation.source), str(operation.destination))
        moved += 1
    return moved
