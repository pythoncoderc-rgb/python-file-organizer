import tempfile
import unittest
from pathlib import Path

from file_organizer.organizer import apply_plan, build_plan, classify_file


class FileOrganizerTests(unittest.TestCase):
    def test_classification_is_case_insensitive(self):
        self.assertEqual(classify_file(Path("photo.JPG")), "Images")
        self.assertEqual(classify_file(Path("script.PY")), "Code")
        self.assertEqual(classify_file(Path("unknown.xyz")), "Other")

    def test_build_plan_does_not_change_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file_path = root / "report.pdf"
            file_path.write_text("x", encoding="utf-8")
            plan = build_plan(root)
            self.assertEqual(len(plan), 1)
            self.assertTrue(file_path.exists())
            self.assertFalse((root / "Documents").exists())

    def test_apply_plan_moves_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "photo.png").write_text("img", encoding="utf-8")
            (root / "notes.txt").write_text("text", encoding="utf-8")
            plan = build_plan(root)
            moved = apply_plan(plan)
            self.assertEqual(moved, 2)
            self.assertTrue((root / "Images" / "photo.png").exists())
            self.assertTrue((root / "Documents" / "notes.txt").exists())

    def test_hidden_files_are_skipped_by_default(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".env").write_text("SECRET=placeholder", encoding="utf-8")
            self.assertEqual(build_plan(root), [])
            self.assertEqual(len(build_plan(root, include_hidden=True)), 1)

    def test_name_collision_gets_suffix(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Documents").mkdir()
            (root / "Documents" / "notes.txt").write_text("old", encoding="utf-8")
            (root / "notes.txt").write_text("new", encoding="utf-8")
            plan = build_plan(root)
            self.assertEqual(plan[0].destination.name, "notes_1.txt")


if __name__ == "__main__":
    unittest.main()
