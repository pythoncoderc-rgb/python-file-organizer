"""Dry-run-first file organization utilities."""

from .organizer import MoveOperation, apply_plan, build_plan, classify_file

__all__ = ["MoveOperation", "apply_plan", "build_plan", "classify_file"]
__version__ = "1.0.0"
