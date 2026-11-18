
import csv
import random
from pathlib import Path

random.seed(42)

OUTPUT = Path(__file__).parent / "messy_products.csv"

products = [
    ("Bezdrátová sluchátka", "Elektronika"),
    ("Herní myš", "Elektronika"),
    ("Mechanická klávesnice", "Elektronika"),
    ("Bavlněné tričko", "Oblečení"),
    ("Pánská mikina", "Oblečení"),
    ("Sportovní láhev", "Sport"),
    ("Jógová podložka", "Sport"),
    ("Kávový mlýnek", "Domácnost"),
    ("Stolní lampa", "Domácnost"),
    ("Batoh", "Doplňky"),
]

rows = []

for i in range(1, 101):
    name, category = random.choice(products)
    sku = f"SKU-{i:04d}"

    # Několik záměrných duplicit
    if i in (25, 50, 75, 100):
        sku = f"SKU-{i - 1:04d}"

    price = random.choice([299, 499, 799, 1299, 2499])
    stock = random.randint(0, 50)

    # Záměrně nekonzistentní data
    messy_category = random.choice([
        category,
        category.upper(),
        f" {category} ",
        category.lower()
    ])

    messy_price = random.choice([
        str(price),
        f"{price},00",
        f"{price} Kč",
        f" {price} "
    ])

    rows.append({
        " SKU ": sku,
        "Product Name": f" {name} " if i % 7 == 0 else name,
        " category ": messy_category,
        "Price CZK": messy_price,
        "stock_quantity": "" if i % 13 == 0 else stock
    })

# Záměrně vytvoříme několik chybějících názvů
for i in (10, 40, 80):
    rows[i - 1]["Product Name"] = ""

with OUTPUT.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys(), delimiter=";")
    writer.writeheader()
    writer.writerows(rows)

print(f"Demo CSV vytvořeno: {OUTPUT}")
print(f"Počet produktů: {len(rows)}")
