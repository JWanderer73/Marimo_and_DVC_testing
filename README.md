# Event pipeline

Run the pipeline from the project directory:

```sh
uv sync --locked
uv run dvc repro
```

The `clean` stage reads `data/raw/events.csv` and writes `data/clean/events.csv`.
It drops rows with any blank fields, event types outside `click`, `view`,
`scroll`, `login`, and `purchase`, or durations less than or equal to zero.
Timestamps are written as `YYYY-MM-DDTHH:MM:SS` (fractional seconds are
discarded), and durations are written as integers.

Input timestamps can use ISO format with optional fractional seconds,
`YYYY-MM-DD HH:MM:SS`, or `MM/DD/YYYY HH:MM:SS`. Unsupported timestamps or
non-integer durations fail the stage so input problems are visible.

The `transform` stage reads `data/clean/events.csv`, adds a `date` column
containing the timestamp's date as `YYYY-MM-DD`, and writes
`data/transformed/events.csv`. Existing columns and row order are preserved.

The `features` stage reads `data/transformed/events.csv` and writes
`data/features/events.csv`, adding `duration_minutes` (`duration_seconds / 60`)
and `weekday` (the full English day name for `date`). All original columns,
row order, and the number of rows are preserved.

All stages run Python through `uv run`; no environment activation is needed.

The raw CSV is tracked with DVC; the original root-level `events.csv` is
preserved. No remote storage is configured yet.

Open the Marimo report after running the pipeline:

```sh
uv run marimo edit notebooks/report.py
```

The notebook loads `data/features/events.csv` and shows a histogram of
`duration_minutes`, with event duration in minutes on the horizontal axis
and event counts on the vertical axis.
