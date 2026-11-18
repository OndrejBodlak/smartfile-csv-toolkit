
import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent


class DemoTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, str(BASE_DIR / "generate_demo.py")],
            check=True
        )
        subprocess.run(
            [sys.executable, str(BASE_DIR / "clean_products.py")],
            check=True
        )

    def test_input_contains_100_products(self):
        with (BASE_DIR / "messy_products.csv").open(
            encoding="utf-8-sig", newline=""
        ) as file:
            rows = list(csv.DictReader(file, delimiter=";"))

        self.assertEqual(len(rows), 100)

    def test_output_contains_96_products(self):
        with (BASE_DIR / "clean_products.csv").open(
            encoding="utf-8-sig", newline=""
        ) as file:
            rows = list(csv.DictReader(file, delimiter=";"))

        self.assertEqual(len(rows), 96)

    def test_skus_are_unique(self):
        with (BASE_DIR / "clean_products.csv").open(
            encoding="utf-8-sig", newline=""
        ) as file:
            rows = list(csv.DictReader(file, delimiter=";"))

        skus = [row["sku"] for row in rows]

        self.assertEqual(len(skus), len(set(skus)))
        self.assertTrue(all(skus))

    def test_prices_have_consistent_format(self):
        with (BASE_DIR / "clean_products.csv").open(
            encoding="utf-8-sig", newline=""
        ) as file:
            rows = list(csv.DictReader(file, delimiter=";"))

        for row in rows:
            self.assertRegex(row["price_czk"], r"^\d+\.\d{2}$")

    def test_report_counts(self):
        with (BASE_DIR / "cleanup_report.json").open(
            encoding="utf-8"
        ) as file:
            report = json.load(file)

        stats = report["statistics"]

        self.assertEqual(stats["rows_read"], 100)
        self.assertEqual(stats["duplicates_removed"], 4)
        self.assertEqual(stats["missing_names"], 3)
        self.assertEqual(stats["missing_stock"], 7)
        self.assertEqual(stats["rows_exported"], 96)


if __name__ == "__main__":
    unittest.main(verbosity=2)
