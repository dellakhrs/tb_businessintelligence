from pathlib import Path

import pandas as pd
import streamlit as st

from database.connection import database_enabled
from database.queries import load_dashboard_datasets
from services.data_quality import (
    clean_packages,
    clean_ratings,
    summarize_clean_ratings,
    validate_source_data,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
AGE_LABELS = ["18-22", "23-27", "28-32", "33-37", "38-42"]


def age_group(series: pd.Series) -> pd.Series:
    return pd.cut(series, bins=[17, 22, 27, 32, 37, 42], labels=AGE_LABELS)


@st.cache_data(show_spinner="Menyiapkan data pariwisata...")
def load_datasets() -> dict[str, pd.DataFrame]:
    if database_enabled():
        try:
            database_datasets = load_dashboard_datasets()
            if database_datasets["places"].empty:
                raise ValueError("tabel dim_destination kosong; jalankan ETL MySQL")
            database_datasets["packages"], package_quality = clean_packages(database_datasets["packages"])
            validate_source_data(
                database_datasets["places"],
                database_datasets["ratings"],
                database_datasets["users"],
                database_datasets["packages"],
            )
            database_datasets["quality"] = summarize_clean_ratings(database_datasets["ratings"])
            database_datasets["quality"].update(package_quality)
            return database_datasets
        except Exception as error:
            st.warning(f"MySQL tidak tersedia, menggunakan fallback CSV: {error}")

    places = pd.read_csv(DATA_DIR / "tourism_with_id.csv")
    ratings = pd.read_csv(DATA_DIR / "tourism_rating.csv")
    users = pd.read_csv(DATA_DIR / "user.csv")
    packages = pd.read_csv(DATA_DIR / "package_tourism.csv")

    places = places.drop(columns=["Unnamed: 11", "Unnamed: 12"], errors="ignore")
    packages, package_quality = clean_packages(packages)
    validate_source_data(places, ratings, users, packages)
    ratings, quality = clean_ratings(ratings)
    quality.update(package_quality)
    users["Age_Group"] = age_group(users["Age"])
    ratings = ratings.merge(users[["User_Id", "Location", "Age", "Age_Group"]], on="User_Id", how="left")
    ratings = ratings.merge(
        places[["Place_Id", "Place_Name", "City", "Category", "Price", "Rating"]],
        on="Place_Id",
        how="left",
    )
    return {
        "places": places,
        "ratings": ratings,
        "users": users,
        "packages": packages,
        "quality": quality,
    }


def get_filter_options(datasets: dict) -> dict:
    places = datasets["places"]
    if places.empty:
        raise ValueError("Dataset destinasi kosong. Jalankan ETL atau periksa sumber data.")
    prices = pd.to_numeric(places["Price"], errors="coerce").dropna()
    ratings = pd.to_numeric(places["Rating"], errors="coerce").dropna()
    if prices.empty or ratings.empty:
        raise ValueError("Kolom Price atau Rating tidak memiliki nilai numerik yang valid.")
    return {
        "cities": sorted(places["City"].unique()),
        "categories": sorted(places["Category"].unique()),
        "price": (int(prices.min()), int(prices.max())),
        "rating": (float(ratings.min()), float(ratings.max())),
        "ages": AGE_LABELS,
    }


def apply_filters(datasets: dict, filters: dict) -> tuple[pd.DataFrame, ...]:
    places = datasets["places"]
    places = places[
        places["City"].isin(filters["cities"])
        & places["Category"].isin(filters["categories"])
        & places["Price"].between(*filters["price"])
        & places["Rating"].between(*filters["rating"])
    ].copy()
    ratings = datasets["ratings"]
    ratings = ratings[
        ratings["Place_Id"].isin(places["Place_Id"]) & ratings["Age_Group"].astype(str).isin(filters["ages"])
    ].copy()
    users = datasets["users"][datasets["users"]["Age_Group"].astype(str).isin(filters["ages"])].copy()
    users = users[users["User_Id"].isin(ratings["User_Id"].unique())]
    packages = datasets["packages"][datasets["packages"]["City"].isin(filters["cities"])].copy()
    return places, ratings, users, packages


def build_analytics(places: pd.DataFrame, ratings: pd.DataFrame, users: pd.DataFrame, packages: pd.DataFrame) -> dict:
    destination_rating = ratings.groupby("Place_Id", as_index=False).agg(
        review_count=("Place_Ratings", "size"),
        user_rating=("Place_Ratings", "mean"),
    )
    destination = places.merge(destination_rating, on="Place_Id", how="left")
    destination[["review_count", "user_rating"]] = destination[["review_count", "user_rating"]].fillna(0)
    destination["rating_gap"] = destination["Rating"] - destination["user_rating"]

    city = destination.groupby("City", as_index=False).agg(
        destinations=("Place_Id", "nunique"),
        avg_price=("Price", "mean"),
        official_rating=("Rating", "mean"),
        user_rating=("user_rating", "mean"),
        review_count=("review_count", "sum"),
    ).sort_values("destinations", ascending=False)

    category = destination.groupby("Category", as_index=False).agg(
        destinations=("Place_Id", "nunique"),
        avg_price=("Price", "mean"),
        official_rating=("Rating", "mean"),
        user_rating=("user_rating", "mean"),
        review_count=("review_count", "sum"),
    )
    place_columns = [column for column in packages.columns if column.startswith("Place_Tourism")]
    package_summary = packages.melt(
        id_vars=["Package", "City"], value_vars=place_columns, value_name="Place"
    ).dropna(subset=["Place"])
    counts = package_summary.groupby("Package").size().rename("places_per_package")
    package_summary = package_summary.merge(counts, on="Package", how="left")

    popular = destination.sort_values(["review_count", "user_rating"], ascending=False)
    top_rated = destination[destination["review_count"] >= 10].sort_values("user_rating", ascending=False)
    gap = destination[destination["review_count"] >= 10].sort_values("rating_gap", ascending=False)

    return {
        "destination": destination,
        "city": city,
        "category": category,
        "popular": popular,
        "top_rated": top_rated,
        "gap": gap,
        "package_summary": package_summary,
    }


def build_actionable_summary(analytics: dict, ratings: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build BPPI promotion indicators and classifications from the active dataset."""
    destinations = analytics["destination"].copy()
    rating_q1 = float(destinations["user_rating"].quantile(0.25))
    rating_q3 = float(destinations["user_rating"].quantile(0.75))
    interaction_median = float(destinations["review_count"].median())
    interaction_q3 = float(destinations["review_count"].quantile(0.75))

    def classify(row: pd.Series) -> str:
        if row["user_rating"] >= rating_q3 and row["review_count"] >= interaction_q3:
            return "Kandidat Promosi Utama"
        if row["user_rating"] >= rating_q3 and row["review_count"] < interaction_median:
            return "Kandidat Promosi Niche"
        if row["user_rating"] <= rating_q1 and row["review_count"] >= interaction_q3:
            return "Perlu Validasi"
        if row["user_rating"] >= rating_q3:
            return "Potensi Pengembangan"
        return "Monitor"

    action_map = {
        "Kandidat Promosi Utama": "Pertimbangkan sebagai materi promosi utama setelah validasi konten.",
        "Kandidat Promosi Niche": "Uji sebagai materi promosi segmen khusus dan tambah bukti interaksi.",
        "Potensi Pengembangan": "Kembangkan eksposur secara bertahap sambil memantau rating.",
        "Perlu Validasi": "Validasi kelayakan dan konteks rating sebelum dipromosikan.",
        "Monitor": "Pantau sebagai bagian dari portofolio destinasi.",
    }
    destinations["Status Promosi"] = destinations.apply(classify, axis=1)
    destinations["Tindakan BPPI"] = destinations["Status Promosi"].map(action_map)
    destinations["Skor Bukti"] = destinations["user_rating"] * destinations["review_count"]

    status_order = [
        "Kandidat Promosi Utama",
        "Kandidat Promosi Niche",
        "Potensi Pengembangan",
        "Perlu Validasi",
        "Monitor",
    ]
    status_counts = (
        destinations["Status Promosi"]
        .value_counts()
        .reindex(status_order, fill_value=0)
        .rename_axis("Status Promosi")
        .reset_index(name="Jumlah Destinasi")
    )

    positive_rating_share = float((ratings["Place_Ratings"] >= 4).mean() * 100)
    indicators = pd.DataFrame(
        [
            {
                "Indikator": "Interaksi Rating Unik",
                "Nilai Tampilan": f"{len(ratings):,}",
                "Definisi": "Jumlah pasangan pengguna-destinasi unik pada filter aktif.",
            },
            {
                "Indikator": "Rating Positif",
                "Nilai Tampilan": f"{positive_rating_share:.1f}%",
                "Definisi": "Persentase rating pengguna bernilai 4 atau 5.",
            },
            {
                "Indikator": "Kandidat Promosi Utama",
                "Nilai Tampilan": f"{int((destinations['Status Promosi'] == 'Kandidat Promosi Utama').sum())} destinasi",
                "Definisi": "Rating dan interaksi berada pada kuartil atas data aktif.",
            },
            {
                "Indikator": "Perlu Validasi",
                "Nilai Tampilan": f"{int((destinations['Status Promosi'] == 'Perlu Validasi').sum())} destinasi",
                "Definisi": "Rating kuartil bawah dengan interaksi kuartil atas.",
            },
        ]
    )

    promotion_priority = destinations[
        destinations["Status Promosi"] == "Kandidat Promosi Utama"
    ].nlargest(8, "Skor Bukti")
    validation_priority = destinations[
        destinations["Status Promosi"] == "Perlu Validasi"
    ].nlargest(7, "Skor Bukti")
    priority_list = pd.concat([promotion_priority, validation_priority], ignore_index=True)
    priority_list["Urutan Status"] = priority_list["Status Promosi"].map(
        {"Kandidat Promosi Utama": 0, "Perlu Validasi": 1}
    )
    priority_list = priority_list.sort_values(
        ["Urutan Status", "Skor Bukti"], ascending=[True, False]
    )

    thresholds = {
        "rating_q1": rating_q1,
        "rating_q3": rating_q3,
        "interaction_median": interaction_median,
        "interaction_q3": interaction_q3,
    }
    return {
        "indicators": indicators,
        "destinations": destinations,
        "status_counts": status_counts,
        "priority_list": priority_list,
        "thresholds": thresholds,
    }
