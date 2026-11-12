import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import csv

    import marimo as mo
    import matplotlib.pyplot as plt

    return csv, mo, plt


@app.cell
def _(csv, mo):
    features_path = mo.notebook_dir().parent / "data" / "features" / "events.csv"
    if not features_path.is_file():
        raise FileNotFoundError(
            f"Missing {features_path}. Run `uv run dvc repro` from the project directory."
        )
    with features_path.open(newline="", encoding="utf-8") as _file:
        duration_minutes = [
            float(_row["duration_minutes"]) for _row in csv.DictReader(_file)
        ]
    return (duration_minutes,)


@app.cell
def _(duration_minutes, mo):
    mo.md(
        f"""
        # Event duration distribution

        Duration in minutes for **{len(duration_minutes):,} events** from
        `data/features/events.csv`. Each bar counts the events in a duration range.
        """
    )
    return


@app.cell
def _(duration_minutes, plt):
    fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    ax.hist(duration_minutes, bins=30, color="#2563eb", edgecolor="white")
    ax.set_title("Distribution of event durations")
    ax.set_xlabel("Event duration (minutes)")
    ax.set_ylabel("Number of events")
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.25)
    fig
    return ax, fig


if __name__ == "__main__":
    app.run()
