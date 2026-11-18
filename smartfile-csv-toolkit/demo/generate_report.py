
import json
import html
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
REPORT_FILE = BASE_DIR / "cleanup_report.json"
OUTPUT_FILE = BASE_DIR / "cleanup_report.html"


def generate_report():
    if not REPORT_FILE.exists():
        raise FileNotFoundError(
            f"Nebyl nalezen report: {REPORT_FILE}"
        )

    with REPORT_FILE.open("r", encoding="utf-8") as file:
        report = json.load(file)

    stats = report.get("statistics", {})

    rows_read = stats.get("rows_read", 0)
    rows_exported = stats.get("rows_exported", 0)
    duplicates = stats.get("duplicates_removed", 0)
    missing_sku = stats.get("missing_sku", 0)
    missing_names = stats.get("missing_names", 0)
    missing_stock = stats.get("missing_stock", 0)
    invalid_prices = stats.get("invalid_prices", 0)
    prices_normalized = stats.get("prices_normalized", 0)
    categories_normalized = stats.get("categories_normalized", 0)
    whitespace_cleaned = stats.get("whitespace_cleaned", 0)

    completion = (
        round(rows_exported / rows_read * 100, 1)
        if rows_read else 0
    )

    missing_values = (
        missing_sku
        + missing_names
        + missing_stock
        + invalid_prices
    )

    generated_at = datetime.now().strftime("%d. %m. %Y v %H:%M")

    def card(value, label, description=""):
        return f"""
        <div class="stat-card">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{html.escape(label)}</div>
            <div class="stat-description">{html.escape(description)}</div>
        </div>
        """

    issues = [
        ("Odstraněné duplicity", duplicates),
        ("Produkty bez SKU", missing_sku),
        ("Chybějící názvy", missing_names),
        ("Chybějící skladové hodnoty", missing_stock),
        ("Neplatné nebo chybějící ceny", invalid_prices),
    ]

    issue_rows = "".join(
        f"""
        <tr>
            <td>{html.escape(label)}</td>
            <td>{value}</td>
        </tr>
        """
        for label, value in issues
    )

    notes = "".join(
        f"<li>{html.escape(note)}</li>"
        for note in report.get("notes", [])
    )

    document = f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Report čištění CSV | SmartFile</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 40px 20px;
    background: #f3f5f7;
    color: #17212b;
    font-family: Arial, sans-serif;
}}

.container {{
    max-width: 1000px;
    margin: auto;
}}

.header {{
    background: #153c2b;
    color: white;
    padding: 35px;
    border-radius: 16px;
    margin-bottom: 25px;
}}

.header h1 {{
    margin: 0 0 10px;
    font-size: 30px;
}}

.header p {{
    color: #d4e8dc;
    margin: 0;
}}

.section {{
    background: white;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}}

.section h2 {{
    margin-top: 0;
    font-size: 20px;
}}

.stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
}}

.stat-card {{
    background: #f7f9f8;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e6ece8;
}}

.stat-value {{
    font-size: 30px;
    font-weight: bold;
    color: #17633f;
}}

.stat-label {{
    font-weight: bold;
    margin-top: 7px;
}}

.stat-description {{
    color: #748078;
    font-size: 12px;
    margin-top: 5px;
}}

.progress {{
    height: 12px;
    background: #e8eee9;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 12px;
}}

.progress-bar {{
    height: 100%;
    width: {completion}%;
    background: #268653;
    border-radius: 20px;
}}

.summary {{
    margin-top: 22px;
    padding: 20px;
    background: #edf5ef;
    border-left: 4px solid #268653;
    border-radius: 10px;
}}

.summary h3 {{
    margin-top: 0;
    color: #153c2b;
}}

.summary p {{
    margin: 8px 0;
    color: #45534a;
    line-height: 1.5;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 13px;
    text-align: left;
    border-bottom: 1px solid #edf0ee;
}}

th {{
    color: #64716a;
    font-size: 13px;
}}

.notes {{
    color: #58645d;
    line-height: 1.8;
}}

.footer {{
    text-align: center;
    color: #8a948e;
    font-size: 13px;
    padding: 15px;
}}

@media (max-width: 600px) {{
    body {{
        padding: 15px 10px;
    }}

    .header {{
        padding: 25px;
    }}

    .section {{
        padding: 18px;
    }}
}}
</style>
</head>

<body>
<div class="container">

    <header class="header">
        <h1>Report čištění CSV</h1>
        <p>SmartFile – přehled zpracování produktových dat</p>
        <p style="margin-top:15px;font-size:13px">
            Vygenerováno: {generated_at}
        </p>
    </header>

    <section class="section">
        <h2>Výsledek zpracování</h2>

        <div class="stats">
            {card(rows_read, "Načtené produkty", "Původní CSV")}
            {card(rows_exported, "Exportované produkty", "Výsledné CSV")}
            {card(duplicates, "Odstraněné duplicity")}
            {card(invalid_prices, "Neplatné ceny")}
        </div>

        <p>
            <strong>Podíl exportovaných produktů: {completion} %</strong>
        </p>

        <div class="progress">
            <div class="progress-bar"></div>
        </div>

        <div class="summary">
            <h3>Shrnutí zpracování</h3>

            <p>
                Bylo načteno
                <strong>{rows_read} produktů</strong>.
            </p>

            <p>
                Bylo odstraněno
                <strong>{duplicates} duplicitních záznamů</strong>.
            </p>

            <p>
                Do výsledného souboru bylo exportováno
                <strong>{rows_exported} produktů</strong>.
            </p>

            <p>
                Bylo zaznamenáno
                <strong>{missing_values} chybějících nebo neplatných hodnot</strong>.
            </p>

            <p>
                Z toho chybějící názvy: <strong>{missing_names}</strong>,
                skladové hodnoty: <strong>{missing_stock}</strong>,
                SKU: <strong>{missing_sku}</strong>,
                ceny: <strong>{invalid_prices}</strong>.
            </p>
        </div>
    </section>

    <section class="section">
        <h2>Provedené úpravy</h2>

        <div class="stats">
            {card(prices_normalized, "Sjednocené ceny")}
            {card(categories_normalized, "Upravené kategorie")}
            {card(whitespace_cleaned, "Odstraněné přebytečné mezery")}
        </div>
    </section>

    <section class="section">
        <h2>Kontrola kvality dat</h2>

        <table>
            <thead>
                <tr>
                    <th>Kontrola</th>
                    <th>Počet</th>
                </tr>
            </thead>

            <tbody>
                {issue_rows}
            </tbody>
        </table>
    </section>

    <section class="section">
        <h2>Poznámky ke zpracování</h2>

        <ul class="notes">
            {notes}
        </ul>
    </section>

    <footer class="footer">
        SmartFile CSV Toolkit · Automatizované čištění dat
    </footer>

</div>
</body>
</html>
"""

    OUTPUT_FILE.write_text(document, encoding="utf-8")

    print("\nHTML REPORT CREATED")
    print("-" * 35)
    print(f"Report: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_report()
