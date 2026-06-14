import pandas as pd

PACKAGE_PLACE_ALIASES = {
    "Ade Irma Suryani Nasution Traffic Park": "Taman Lalu Lintas Ade Irma Suryani Nasution",
    "Gunung Tangkuban Perahu": "GunungTangkuban perahu",
    "Monas": "Monumen Nasional",
    "Semarang Gallery": "Semarang Contemporary Art Gallery",
    "Stone Garden Geopark": "Stone Garden Citatah",
    "Taman Pelangi Jogja": "Taman Pelangi Yogyakarta",
    "Wisata Kalibiru": "Wisata Alam Kalibiru",
}


def clean_packages(packages: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    cleaned = packages.copy()
    place_columns = [column for column in cleaned if column.startswith("Place_Tourism")]
    normalized_values = 0
    aliased_values = 0

    for column in place_columns:
        original = cleaned[column].copy()
        normalized = original.apply(
            lambda value: value.strip().removeprefix("|").strip() if isinstance(value, str) else value
        )
        normalized_values += int((original.fillna("") != normalized.fillna("")).sum())
        aliased = normalized.replace(PACKAGE_PLACE_ALIASES)
        aliased_values += int((normalized.fillna("") != aliased.fillna("")).sum())
        cleaned[column] = aliased

    return cleaned, {
        "normalized_package_place_names": normalized_values,
        "aliased_package_place_names": aliased_values,
    }


def validate_source_data(
    places: pd.DataFrame,
    ratings: pd.DataFrame,
    users: pd.DataFrame,
    packages: pd.DataFrame | None = None,
) -> None:
    if places["Place_Id"].duplicated().any():
        raise ValueError("Place_Id harus unik pada dataset destinasi.")
    if users["User_Id"].duplicated().any():
        raise ValueError("User_Id harus unik pada dataset pengguna.")
    if not ratings["Place_Ratings"].between(1, 5).all():
        raise ValueError("Place_Ratings harus berada pada rentang 1 sampai 5.")
    if not places["Rating"].between(1, 5).all():
        raise ValueError("Rating referensi dataset harus berada pada rentang 1 sampai 5.")
    if (places["Price"] < 0).any():
        raise ValueError("Harga destinasi tidak boleh bernilai negatif.")
    if not ratings["Place_Id"].isin(places["Place_Id"]).all():
        raise ValueError("Terdapat Place_Id rating yang tidak ditemukan pada dataset destinasi.")
    if not ratings["User_Id"].isin(users["User_Id"]).all():
        raise ValueError("Terdapat User_Id rating yang tidak ditemukan pada dataset pengguna.")
    if packages is not None:
        if packages["Package"].duplicated().any():
            raise ValueError("Package harus unik pada dataset paket wisata.")
        place_columns = [column for column in packages if column.startswith("Place_Tourism")]
        package_places = packages[place_columns].stack().dropna()
        if not package_places.isin(places["Place_Name"]).all():
            raise ValueError("Terdapat destinasi paket yang tidak ditemukan pada dataset destinasi.")


def clean_ratings(ratings: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    raw_rows = len(ratings)
    exact_clean = ratings.drop_duplicates().copy()
    exact_duplicates_removed = raw_rows - len(exact_clean)

    cleaned = exact_clean.groupby(["User_Id", "Place_Id"], as_index=False).agg(
        Place_Ratings=("Place_Ratings", "mean"),
        Rating_Observations=("Place_Ratings", "size"),
    )
    repeated_pairs = int((cleaned["Rating_Observations"] > 1).sum())
    repeated_observations_merged = int(cleaned["Rating_Observations"].sum() - len(cleaned))

    quality = {
        "raw_rating_rows": raw_rows,
        "exact_duplicates_removed": exact_duplicates_removed,
        "repeated_user_destination_pairs": repeated_pairs,
        "repeated_observations_merged": repeated_observations_merged,
        "represented_rating_observations": int(cleaned["Rating_Observations"].sum()),
        "clean_rating_rows": len(cleaned),
    }
    return cleaned, quality


def summarize_clean_ratings(ratings: pd.DataFrame) -> dict[str, int]:
    observations = (
        int(ratings["Rating_Observations"].sum())
        if "Rating_Observations" in ratings
        else len(ratings)
    )
    return {
        "raw_rating_rows": observations,
        "exact_duplicates_removed": 0,
        "repeated_user_destination_pairs": int(
            (ratings.get("Rating_Observations", pd.Series(1, index=ratings.index)) > 1).sum()
        ),
        "repeated_observations_merged": observations - len(ratings),
        "represented_rating_observations": observations,
        "clean_rating_rows": len(ratings),
    }
