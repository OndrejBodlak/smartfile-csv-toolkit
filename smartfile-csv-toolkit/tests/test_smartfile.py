import tempfile
import unittest
from pathlib import Path

from smartfile import read_csv, remove_duplicates, write_csv


class SmartFileTests(unittest.TestCase):
    def test_reads_and_trims_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.csv"
            path.write_text(" name , email \n Alice , a@example.com \n", encoding="utf-8")
            headers, rows, delimiter = read_csv(path)
            self.assertEqual(headers, ["name", "email"])
            self.assertEqual(rows, [{"name": "Alice", "email": "a@example.com"}])
            self.assertEqual(delimiter, ",")

    def test_removes_duplicate_rows(self):
        rows = [
            {"name": "Alice", "email": "a@example.com"},
            {"name": "Alice", "email": "a@example.com"},
            {"name": "Bob", "email": "b@example.com"},
        ]
        unique, removed = remove_duplicates(rows, ["name", "email"])
        self.assertEqual(len(unique), 2)
        self.assertEqual(removed, 1)

    def test_writes_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.csv"
            write_csv(path, ["name"], [{"name": "Alice"}])
            self.assertTrue(path.exists())
            self.assertIn("Alice", path.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
