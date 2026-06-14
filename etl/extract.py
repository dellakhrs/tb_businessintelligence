"""Extract tourism source data from CSV files."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def extract() -> dict[str, pd.DataFrame]:
    """Read all source CSV files required by the tourism ETL."""
    return {
        "places": pd.read_csv(DATA / "tourism_with_id.csv"),
        "ratings": pd.read_csv(DATA / "tourism_rating.csv"),
        "users": pd.read_csv(DATA / "user.csv"),
        "packages": pd.read_csv(DATA / "package_tourism.csv"),
    }
