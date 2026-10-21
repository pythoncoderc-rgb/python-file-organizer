from __future__ import annotations

import argparse
from pathlib import Path

from .organizer import apply_plan, build_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Preview or apply a simple extension-based file organization plan.",
    )
    parser.add_argument("directory", nargs="?", default=".", help="directory to organize")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="move files; without this flag the command is dry-run only",
    )
    parser.add_argument("--include-hidden", action="store_true", help="include dotfiles")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    directory = Path(args.directory)

    try:
        plan = build_plan(directory, include_hidden=args.include_hidden)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"Error: {exc}")
        return 2

    if not plan:
        print("No files to organize.")
        return 0

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"{mode}: {len(plan)} file(s)")
    for operation in plan:
        print(f"  {operation.source.name} -> {operation.category}/{operation.destination.name}")

    if not args.apply:
        print("No files were changed. Run again with --apply to perform the moves.")
        return 0

    moved = apply_plan(plan)
    print(f"Moved {moved} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
