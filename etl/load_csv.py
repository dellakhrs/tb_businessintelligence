"""Run the complete tourism CSV-to-MySQL ETL pipeline."""

from etl.extract import extract
from etl.load import create_schema, load
from etl.transform import transform


def run_etl() -> None:
    tables = transform(extract())
    create_schema()
    load(tables)
    print("ETL MySQL selesai.")


if __name__ == "__main__":
    run_etl()
