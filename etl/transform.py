"""Transform tourism source data into star-schema tables."""

import pandas as pd

from services.data_quality import clean_packages, clean_ratings, validate_source_data

AGE_LABELS = ["18-22", "23-27", "28-32", "33-37", "38-42"]


def transform(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Clean, validate, and reshape source data into dimensions and facts."""
    places = raw["places"].drop(columns=["Unnamed: 11", "Unnamed: 12"], errors="ignore")
    users = raw["users"].copy()
    packages, _ = clean_packages(raw["packages"])
    validate_source_data(places, raw["ratings"], users, packages)
    ratings, _ = clean_ratings(raw["ratings"])

    users["Age_Group"] = pd.cut(
        users["Age"],
        [17, 22, 27, 32, 37, 42],
        labels=AGE_LABELS,
    ).astype(str)

    cities = pd.DataFrame({"City": sorted(places["City"].unique())})
    cities.insert(0, "City_Id", range(1, len(cities) + 1))

    categories = pd.DataFrame({"Category": sorted(places["Category"].unique())})
    categories.insert(0, "Category_Id", range(1, len(categories) + 1))

    destinations = places.merge(cities, on="City").merge(categories, on="Category")
    destinations = destinations.drop(columns=["City", "Category"])[
        [
            "Place_Id",
            "Place_Name",
            "Description",
            "City_Id",
            "Category_Id",
            "Price",
            "Rating",
            "Time_Minutes",
            "Coordinate",
            "Lat",
            "Long",
        ]
    ]

    dim_packages = packages[["Package", "City"]].merge(cities, on="City")
    dim_packages = dim_packages.rename(columns={"Package": "Package_Id"})[
        ["Package_Id", "City_Id"]
    ]

    place_columns = [column for column in packages if column.startswith("Place_Tourism")]
    bridge = packages.melt(
        id_vars="Package",
        value_vars=place_columns,
        var_name="Sequence",
        value_name="Place_Name",
    ).dropna()
    bridge["Sequence_No"] = bridge["Sequence"].str.extract(r"(\d+)").astype(int)
    bridge = bridge.merge(places[["Place_Id", "Place_Name"]], on="Place_Name")
    bridge = bridge.rename(columns={"Package": "Package_Id"})[
        ["Package_Id", "Place_Id", "Sequence_No"]
    ]

    return {
        "dim_city": cities,
        "dim_category": categories,
        "dim_destination": destinations,
        "dim_user": users,
        "fact_rating": ratings,
        "dim_package": dim_packages,
        "bridge_package_destination": bridge,
    }
