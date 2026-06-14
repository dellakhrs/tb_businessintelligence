"""Create the MySQL star schema and load transformed tourism tables."""

import os
import shutil
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from database.connection import get_engine, get_server_engine

ROOT = Path(__file__).resolve().parents[1]
DELETE_ORDER = [
    "bridge_package_destination",
    "fact_rating",
    "dim_package",
    "dim_destination",
    "dim_user",
    "dim_category",
    "dim_city",
]
LOAD_ORDER = [
    "dim_city",
    "dim_category",
    "dim_destination",
    "dim_user",
    "dim_package",
    "bridge_package_destination",
    "fact_rating",
]


def create_schema() -> None:
    """Create the database and execute the star-schema SQL definition."""
    database = os.getenv("DB_NAME", "bi_pariwisata")
    with get_server_engine().begin() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{database}`"))

    statements = [
        sql.strip()
        for sql in (ROOT / "sql/schema.sql").read_text().split(";")
        if sql.strip()
    ]
    with get_engine().begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def load(tables: dict[str, pd.DataFrame]) -> None:
    """Replace MySQL star-schema table contents with transformed data."""
    free_space = shutil.disk_usage(ROOT).free
    if free_space < 512 * 1024 * 1024:
        raise RuntimeError(
            f"Ruang disk tidak cukup: {free_space / 1024 / 1024:.0f} MB tersedia. "
            "Kosongkan minimal 512 MB sebelum ETL."
        )

    engine = get_engine()
    with engine.begin() as connection:
        for table in DELETE_ORDER:
            connection.execute(text(f"DELETE FROM {table}"))

    for table in LOAD_ORDER:
        tables[table].to_sql(
            table,
            engine,
            if_exists="append",
            index=False,
            chunksize=1_000,
        )
        print(f"{table}: {len(tables[table]):,} baris")
