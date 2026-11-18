
import csv
import json
from pathlib import Path
from collections import Counter
from decimal import Decimal, InvalidOperation

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "messy_products.csv"
OUTPUT_FILE = BASE_DIR / "clean_products.csv"
REPORT_FILE = BASE_DIR / "cleanup_report.json"


def normalize_price(value):
    """Převede cenu do jednotného formátu 0.00."""
    value = str(value or "").strip()
    value = value.replace("Kč", "").replace("\u00a0", "").replace(" ", "")

    if not value:
        return ""

    # Český formát: 1.299,00 -> 1299.00
    if "," in value:
        value = value.replace(".", "").replace(",", ".")

    try:
        price = Decimal(value)

        if not price.is_finite() or price < 0:
            return ""

        return f"{price:.2f}"

    except InvalidOperation:
        return ""


def clean_products():
    stats = Counter()
    cleaned_rows = []
    seen_skus = set()

    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            stats["rows_read"] += 1

            raw_sku = row.get(" SKU ", "") or ""
            raw_name = row.get("Product Name", "") or ""
            raw_category = row.get(" category ", "") or ""
            raw_price = row.get("Price CZK", "") or ""
            raw_stock = row.get("stock_quantity", "") or ""

            # Odstranění přebytečných mezer
            values = [
                raw_sku, raw_name, raw_category, raw_price, raw_stock
            ]
            stats["whitespace_cleaned"] += sum(
                1 for value in values if value != value.strip()
            )

            sku = raw_sku.strip()
            name = raw_name.strip()
            category = raw_category.strip().title()
            price = normalize_price(raw_price)
            stock = raw_stock.strip()

            # Chybějící SKU
            if not sku:
                stats["missing_sku"] += 1
                continue

            # Duplicitní SKU (bez rozlišení velikosti písmen)
            sku_key = sku.casefold()

            if sku_key in seen_skus:
                stats["duplicates_removed"] += 1
                continue

            seen_skus.add(sku_key)

            # Kontrola názvu
            if not name:
                stats["missing_names"] += 1

            # Kontrola ceny
            if not price:
                stats["invalid_prices"] += 1
            elif price != raw_price.strip():
                stats["prices_normalized"] += 1

            # Kontrola kategorie
            if category != raw_category.strip():
                stats["categories_normalized"] += 1

            # Kontrola skladu
            if not stock:
                stats["missing_stock"] += 1

            cleaned_rows.append({
                "sku": sku,
                "name": name,
                "category": category,
                "price_czk": price,
                "stock_quantity": stock
            })

    fieldnames = [
        "sku",
        "name",
        "category",
        "price_czk",
        "stock_quantity"
    ]

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(cleaned_rows)

    stats["rows_exported"] = len(cleaned_rows)

    report = {
        "input_file": INPUT_FILE.name,
        "output_file": OUTPUT_FILE.name,
        "statistics": dict(stats),
        "notes": [
            "Všechna produktová data v této ukázce jsou fiktivní.",
            "Ceny jsou sjednoceny na dvě desetinná místa.",
            "Neplatné nebo chybějící ceny zůstávají prázdné.",
            "Záporné a nekonečné ceny jsou odmítnuty.",
            "Produkty bez SKU jsou vyřazeny.",
            "Duplicity SKU jsou rozpoznávány bez ohledu na velikost písmen.",
            "Při duplicitě je zachován první výskyt produktu.",
            "Chybějící názvy a skladové hodnoty jsou zaznamenány."
        ]
    }

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=4)

    print("\nCSV CLEANUP COMPLETED")
    print("-" * 35)

    for key, value in stats.items():
        print(f"{key}: {value}")

    print(f"\nCleaned CSV: {OUTPUT_FILE}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    clean_products()
