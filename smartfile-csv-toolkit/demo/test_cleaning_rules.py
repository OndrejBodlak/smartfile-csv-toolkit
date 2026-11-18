
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

import clean_products


class CleaningRulesTests(unittest.TestCase):

    def test_duplicate_and_missing_sku_handling(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)

            input_file = temp / "input.csv"
            output_file = temp / "output.csv"
            report_file = temp / "report.json"

            rows = [
                {
                    " SKU ": "ABC-001",
                    "Product Name": "First product",
                    " category ": "Electronics",
                    "Price CZK": "299",
                    "stock_quantity": "10"
                },
                {
                    " SKU ": "abc-001",
                    "Product Name": "Duplicate product",
                    " category ": "Electronics",
                    "Price CZK": "399",
                    "stock_quantity": "5"
                },
                {
                    " SKU ": "",
                    "Product Name": "Product without SKU",
                    " category ": "Sport",
                    "Price CZK": "199",
                    "stock_quantity": "3"
                },
                {
                    " SKU ": "XYZ-002",
                    "Product Name": "Second product",
                    " category ": "Sport",
                    "Price CZK": "499",
                    "stock_quantity": "7"
                }
            ]

            with input_file.open(
                "w", encoding="utf-8-sig", newline=""
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        " SKU ",
                        "Product Name",
                        " category ",
                        "Price CZK",
                        "stock_quantity"
                    ],
                    delimiter=";"
                )
                writer.writeheader()
                writer.writerows(rows)

            with patch.object(clean_products, "INPUT_FILE", input_file), \
                 patch.object(clean_products, "OUTPUT_FILE", output_file), \
                 patch.object(clean_products, "REPORT_FILE", report_file):

                with redirect_stdout(StringIO()):
                    clean_products.clean_products()

            with output_file.open(
                encoding="utf-8-sig", newline=""
            ) as file:
                result = list(csv.DictReader(file, delimiter=";"))

            self.assertEqual(len(result), 2)
            self.assertEqual(
                [row["sku"] for row in result],
                ["ABC-001", "XYZ-002"]
            )
            self.assertEqual(result[0]["name"], "First product")

            import json

            report = json.loads(report_file.read_text(encoding="utf-8"))

            self.assertEqual(
                report["statistics"]["duplicates_removed"], 1
            )
            self.assertEqual(
                report["statistics"]["missing_sku"], 1
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
