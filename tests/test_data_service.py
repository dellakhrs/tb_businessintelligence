from pathlib import Path

from services.data_service import (
    apply_filters,
    build_actionable_summary,
    build_analytics,
    get_filter_options,
    load_datasets,
)


def test_dashboard_has_four_pages_and_required_visuals() -> None:
    source = Path("app.py").read_text(encoding="utf-8")
    expected_pages = [
        '"Dashboard Overview"',
        '"Destinasi & Kategori"',
        '"Paket & Harga"',
        '"Halaman 5"',
    ]
    required_overview_visuals = [
        "Distribusi Destinasi per Kategori",
        "Kota dengan Destinasi Terbanyak",
        "Volume Interaksi Rating Wisatawan per Kota",
        "Peta Sebaran Destinasi",
        "Distribusi Status Prioritas",
    ]
    required_destination_visuals = [
        "Rating Pengguna Rata-rata per Kategori",
        "Struktur Harga per Kategori",
        "Top 10 Destinasi Berdasarkan Rating Pengguna",
    ]
    required_price_visuals = [
        "Harga Rata-rata Tiket per Kategori (Rp)",
        "Distribusi Tier Harga Keseluruhan Destinasi",
    ]

    pages_block = source[source.index("PAGES = ["):source.index("PAGE_LABELS = {")]
    assert all(page in pages_block for page in expected_pages)
    assert pages_block.count('    "') == 4
    assert all(title in source for title in required_overview_visuals)
    assert all(title in source for title in required_destination_visuals)
    assert "Rating Referensi Dataset Rata-rata per Kategori" not in source
    assert all(title in source for title in required_price_visuals)
    assert 'CHART_PALETTE = ["#174A7E", "#2F6690", "#4E83B6", "#6E9FAD", "#89A9C1", "#AFC6D6"]' in source
    assert '"Executive Dashboard"' not in pages_block
    overview_block = source[source.index('if page == "Dashboard Overview"'):source.index('elif page == "Destinasi & Kategori"')]
    assert "metric_row([" in overview_block
    assert "Prioritas & Tindakan BPPI" in overview_block
    assert "Alert prioritas:" not in overview_block
    assert "Benchmark data aktif:" not in overview_block
    assert "Daftar Tindakan Prioritas" in overview_block
    assert "Rekomendasi Tindakan" in overview_block
    assert "Filter Status Prioritas" in overview_block
    assert 'actionable["destinations"][' in overview_block


def test_dashboard_copy_avoids_unsupported_claims() -> None:
    dashboard_source = open("app.py", encoding="utf-8").read().lower()
    unsupported_claims = [
        "distribusi bimodal",
        "wisatawan cenderung terpolarisasi",
        "sampel populasi yang besar dan representatif",
        "direkomendasikan",
        "rating kualitas",
        "skor kualitas",
        "destinasi terbaik per rupiah",
        "ambang batas minimum (3.0)",
        "threshold evaluasi kritis",
    ]
    assert not any(claim in dashboard_source for claim in unsupported_claims)


def test_cleaned_dataset_and_relationships() -> None:
    datasets = load_datasets()
    assert len(datasets["places"]) == 437
    assert len(datasets["ratings"]) == 9_597
    assert not datasets["ratings"].duplicated(["User_Id", "Place_Id"]).any()
    assert datasets["ratings"]["Rating_Observations"].sum() == 9_921
    assert datasets["ratings"]["Place_Id"].isin(datasets["places"]["Place_Id"]).all()
    assert datasets["ratings"]["User_Id"].isin(datasets["users"]["User_Id"]).all()
    assert datasets["ratings"]["Place_Ratings"].between(1, 5).all()
    assert datasets["places"]["Rating"].between(1, 5).all()
    assert datasets["places"]["Price"].ge(0).all()
    assert datasets["quality"] == {
        "raw_rating_rows": 10_000,
        "exact_duplicates_removed": 79,
        "repeated_user_destination_pairs": 319,
        "repeated_observations_merged": 324,
        "represented_rating_observations": 9_921,
        "clean_rating_rows": 9_597,
        "normalized_package_place_names": 5,
        "aliased_package_place_names": 8,
    }


def test_analytics_respects_full_filters() -> None:
    datasets = load_datasets()
    options = get_filter_options(datasets)
    filters = {
        "cities": options["cities"],
        "categories": options["categories"],
        "price": options["price"],
        "rating": options["rating"],
        "ages": options["ages"],
    }
    places, ratings, users, packages = apply_filters(datasets, filters)
    analytics = build_analytics(places, ratings, users, packages)
    assert analytics["city"]["destinations"].sum() == 437
    assert analytics["popular"].iloc[0]["Place_Name"] == "Gunung Lalakon"


def test_promotion_summary_uses_dataset_benchmarks() -> None:
    datasets = load_datasets()
    options = get_filter_options(datasets)
    filters = {
        "cities": options["cities"],
        "categories": options["categories"],
        "price": options["price"],
        "rating": options["rating"],
        "ages": options["ages"],
    }
    places, ratings, users, packages = apply_filters(datasets, filters)
    actionable = build_actionable_summary(build_analytics(places, ratings, users, packages), ratings)

    destinations = actionable["destinations"]
    thresholds = actionable["thresholds"]
    allowed_statuses = {
        "Kandidat Promosi Utama",
        "Kandidat Promosi Niche",
        "Potensi Pengembangan",
        "Perlu Validasi",
        "Monitor",
    }

    assert len(actionable["indicators"]) == 4
    assert destinations["Status Promosi"].notna().all()
    assert set(destinations["Status Promosi"]).issubset(allowed_statuses)
    assert actionable["status_counts"]["Jumlah Destinasi"].sum() == len(destinations)
    assert len(actionable["priority_list"]) <= 15
    assert set(actionable["priority_list"]["Status Promosi"]).issubset(
        {"Kandidat Promosi Utama", "Perlu Validasi"}
    )
    assert set(actionable["priority_list"]["Status Promosi"]) == {
        "Kandidat Promosi Utama",
        "Perlu Validasi",
    }
    assert thresholds["rating_q1"] == destinations["user_rating"].quantile(0.25)
    assert thresholds["rating_q3"] == destinations["user_rating"].quantile(0.75)
    assert thresholds["interaction_median"] == destinations["review_count"].median()
    assert thresholds["interaction_q3"] == destinations["review_count"].quantile(0.75)


def test_promotion_benchmarks_respect_active_filters() -> None:
    datasets = load_datasets()
    options = get_filter_options(datasets)
    full_filters = {
        "cities": options["cities"],
        "categories": options["categories"],
        "price": options["price"],
        "rating": options["rating"],
        "ages": options["ages"],
    }
    city_filters = {**full_filters, "cities": ["Jakarta"]}

    full = apply_filters(datasets, full_filters)
    jakarta = apply_filters(datasets, city_filters)
    full_summary = build_actionable_summary(build_analytics(*full), full[1])
    jakarta_summary = build_actionable_summary(build_analytics(*jakarta), jakarta[1])

    assert len(jakarta_summary["destinations"]) < len(full_summary["destinations"])
    assert jakarta_summary["status_counts"]["Jumlah Destinasi"].sum() == len(jakarta_summary["destinations"])
    assert jakarta_summary["thresholds"] != full_summary["thresholds"]
