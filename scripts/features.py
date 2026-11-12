"""Add duration in minutes and English weekday names to transformed events."""

import argparse
import csv
from datetime import date
from pathlib import Path


WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def features(source: Path, destination: Path) -> int:
    with source.open(newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        if not {"duration_seconds", "date"}.issubset(reader.fieldnames or []):
            raise ValueError("Input CSV is missing duration_seconds or date")
        fieldnames = list(reader.fieldnames)
        for column in ("duration_minutes", "weekday"):
            if column not in fieldnames:
                fieldnames.append(column)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            count = 0
            for row in reader:
                row["duration_minutes"] = str(int(row["duration_seconds"]) / 60)
                row["weekday"] = WEEKDAYS[date.fromisoformat(row["date"]).weekday()]
                writer.writerow(row)
                count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path, default=Path("data/transformed/events.csv")
    )
    parser.add_argument("--output", type=Path, default=Path("data/features/events.csv"))
    args = parser.parse_args()
    count = features(args.input, args.output)
    print(f"Added features to {count} rows.")
