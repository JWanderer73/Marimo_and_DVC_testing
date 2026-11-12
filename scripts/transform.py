"""Add a date column to cleaned events."""

import argparse
import csv
from datetime import datetime
from pathlib import Path


def transform(source: Path, destination: Path) -> int:
    with source.open(newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        if not reader.fieldnames or "timestamp" not in reader.fieldnames:
            raise ValueError("Input CSV is missing the timestamp column")
        fieldnames = list(reader.fieldnames)
        if "date" not in fieldnames:
            fieldnames.append("date")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            count = 0
            for row in reader:
                row["date"] = datetime.strptime(
                    row["timestamp"], "%Y-%m-%dT%H:%M:%S"
                ).date().isoformat()
                writer.writerow(row)
                count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/clean/events.csv"))
    parser.add_argument(
        "--output", type=Path, default=Path("data/transformed/events.csv")
    )
    args = parser.parse_args()
    count = transform(args.input, args.output)
    print(f"Transformed {count} rows.")
