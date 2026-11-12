"""Filter event records and normalize their timestamps and durations."""

import argparse
import csv
from datetime import datetime
from pathlib import Path


VALID_EVENT_TYPES = {"click", "view", "scroll", "login", "purchase"}
TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
)
REQUIRED_FIELDS = {"user_id", "timestamp", "event_type", "duration_seconds"}


def normalize_timestamp(value: str) -> str:
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(value, fmt).isoformat(timespec="seconds")
        except ValueError:
            continue
    raise ValueError(f"Unsupported timestamp: {value!r}")


def clean(source: Path, destination: Path) -> tuple[int, int]:
    with source.open(newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        if not REQUIRED_FIELDS.issubset(reader.fieldnames or []):
            raise ValueError("Input CSV is missing required columns")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            total = kept = 0
            for row in reader:
                total += 1
                if any(value is None or not value.strip() for value in row.values()):
                    continue
                if row["event_type"] not in VALID_EVENT_TYPES:
                    continue
                duration = int(row["duration_seconds"])
                if duration <= 0:
                    continue
                row["timestamp"] = normalize_timestamp(row["timestamp"])
                row["duration_seconds"] = str(duration)
                writer.writerow(row)
                kept += 1
    return total, kept


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/raw/events.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/clean/events.csv"))
    args = parser.parse_args()
    total, kept = clean(args.input, args.output)
    print(f"Cleaned {total} rows: kept {kept}, dropped {total - kept}.")
