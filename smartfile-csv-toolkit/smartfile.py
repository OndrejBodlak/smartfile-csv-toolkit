#!/usr/bin/env python3
"""SmartFile CSV Toolkit - local CSV cleaning, merging and statistics."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]], str]:
    """Read a CSV file, supporting UTF-8 BOM and comma/semicolon delimiters."""
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise ValueError(f"Cannot read '{path}': {exc}") from exc

    if not raw.strip():
        raise ValueError(f"'{path}' is empty.")

    try:
        dialect = csv.Sniffer().sniff(raw[:8192], delimiters=",;\t|")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ","

    reader = csv.DictReader(raw.splitlines(), delimiter=delimiter)
    if not reader.fieldnames:
        raise ValueError(f"'{path}' does not contain a header row.")

    headers = [str(h or "").strip() for h in reader.fieldnames]
    if not any(headers):
        raise ValueError(f"'{path}' has an empty header row.")
    if len(set(headers)) != len(headers):
        raise ValueError(f"'{path}' contains duplicate column names.")

    rows: list[dict[str, str]] = []
    for raw_row in reader:
        row = {}
        for old_key, value in raw_row.items():
            key = str(old_key or "").strip()
            if key:
                row[key] = (value or "").strip()
        # Ignore rows that are completely empty.
        if any(value for value in row.values()):
            rows.append(row)

    return headers, rows, delimiter


def write_csv(path: Path, headers: list[str], rows: Iterable[dict[str, str]],
              delimiter: str = ",") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=headers, delimiter=delimiter,
                extrasaction="ignore", lineterminator="\n"
            )
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        raise ValueError(f"Cannot write '{path}': {exc}") from exc


def remove_duplicates(rows: list[dict[str, str]], headers: list[str]) -> tuple[list[dict[str, str]], int]:
    seen = set()
    unique = []
    removed = 0
    for row in rows:
        key = tuple(row.get(header, "") for header in headers)
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        unique.append(row)
    return unique, removed


def command_clean(args: argparse.Namespace) -> int:
    headers, rows, delimiter = read_csv(args.input)
    before = len(rows)
    removed = 0
    if args.dedupe:
        rows, removed = remove_duplicates(rows, headers)
    write_csv(args.output, headers, rows, delimiter)
    print(f"Input rows:       {before}")
    print(f"Duplicates removed: {removed}")
    print(f"Output rows:      {len(rows)}")
    print(f"Saved to:         {args.output}")
    return 0


def command_merge(args: argparse.Namespace) -> int:
    all_headers: list[str] = []
    all_rows: list[dict[str, str]] = []
    for path in args.inputs:
        headers, rows, _ = read_csv(path)
        for header in headers:
            if header not in all_headers:
                all_headers.append(header)
        all_rows.extend(rows)

    before = len(all_rows)
    removed = 0
    if args.dedupe:
        all_rows, removed = remove_duplicates(all_rows, all_headers)
    write_csv(args.output, all_headers, all_rows, args.delimiter)
    print(f"Files merged:       {len(args.inputs)}")
    print(f"Input rows:         {before}")
    print(f"Duplicates removed: {removed}")
    print(f"Output rows:        {len(all_rows)}")
    print(f"Columns:            {len(all_headers)}")
    print(f"Saved to:           {args.output}")
    return 0


def command_stats(args: argparse.Namespace) -> int:
    headers, rows, _ = read_csv(args.input)
    print(f"File: {args.input}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(headers)}")
    print("Column names:")
    for header in headers:
        filled = sum(bool(row.get(header, "")) for row in rows)
        print(f"  - {header}: {filled}/{len(rows)} filled")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smartfile",
        description="Clean, merge and inspect CSV files locally."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    clean = subparsers.add_parser("clean", help="Clean one CSV file.")
    clean.add_argument("input", type=Path, help="Input CSV file")
    clean.add_argument("-o", "--output", type=Path, required=True, help="Output CSV file")
    clean.add_argument("--dedupe", action="store_true", help="Remove identical rows")
    clean.set_defaults(func=command_clean)

    merge = subparsers.add_parser("merge", help="Merge multiple CSV files.")
    merge.add_argument("inputs", nargs="+", type=Path, help="Input CSV files")
    merge.add_argument("-o", "--output", type=Path, required=True, help="Output CSV file")
    merge.add_argument("--dedupe", action="store_true", help="Remove identical rows")
    merge.add_argument("--delimiter", choices=[",", ";", "\t"], default=",",
                       help="Output delimiter (default: comma)")
    merge.set_defaults(func=command_merge)

    stats = subparsers.add_parser("stats", help="Show basic CSV statistics.")
    stats.add_argument("input", type=Path, help="Input CSV file")
    stats.set_defaults(func=command_stats)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
