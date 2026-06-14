import pandas as pd
import plotly.express as px
import streamlit as st
from components.ui import (
    COLORS,
    inject_css,
    metric_card,
    page_header,
    render_empty_state,
    render_footer,
    render_app_sidebar,
    section_header,
)
from services.data_service import (
    apply_filters,
    build_actionable_summary,
    build_analytics,
    get_filter_options,
    load_datasets,
)

st.set_page_config(
    page_title="BPPI | Prioritas Promosi Pariwisata",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

PAGES = [
    "Dashboard Overview",
    "Destinasi & Kategori",
    "Paket & Harga",
]

PAGE_LABELS = {
    "Dashboard Overview": "Dashboard Overview",
    "Destinasi & Kategori": "Destinasi & Kategori",
    "Paket & Harga": "Paket & Harga",
}
CHART_PALETTE = ["#174A7E", "#2F6690", "#4E83B6", "#6E9FAD", "#89A9C1", "#AFC6D6"]
CATEGORY_COLORS = {
    "Taman Hiburan": "#174A7E",
    "Budaya": "#2F6690",
    "Cagar Alam": "#4E83B6",
    "Bahari": "#6E9FAD",
    "Tempat Ibadah": "#89A9C1",
    "Pusat Perbelanjaan": "#AFC6D6",
}
CITY_COLORS = {
    "Yogyakarta": "#174A7E",
    "Bandung": "#2F6690",
    "Jakarta": "#4E83B6",
    "Semarang": "#6E9FAD",
    "Surabaya": "#89A9C1",
}
PRICE_TIER_ORDER = [
    "Gratis",
    "Terjangkau (>Rp0-25 ribu)",
    "Menengah (>Rp25-75 ribu)",
    "Tinggi (>Rp75-300 ribu)",
    "Premium (>Rp300 ribu)",
]
PRICE_TIER_COLORS = {
    "Gratis": "#AFC6D6",
    "Terjangkau (>Rp0-25 ribu)": "#6E9FAD",
    "Menengah (>Rp25-75 ribu)": "#4E83B6",
    "Tinggi (>Rp75-300 ribu)": "#2F6690",
    "Premium (>Rp300 ribu)": "#174A7E",
}
CHART_LABELS = {
    "City": "Kota",
    "Category": "Kategori",
    "destinations": "Jumlah Destinasi",
    "avg_price": "Harga Rata-rata",
    "official_rating": "Rating Referensi Dataset",
    "user_rating": "Rating Pengguna",
    "review_count": "Jumlah Interaksi Rating",
    "rating_gap": "Selisih Rating Referensi - Pengguna",
    "Price": "Harga Tiket",
    "Rating": "Rating Referensi Dataset",
    "Place_Name": "Destinasi",
    "Place_Ratings": "Rating Pengguna",
    "Age_Group": "Kelompok Usia",
    "Location": "Asal Pengguna",
    "Package": "Paket Wisata",
    "places_per_package": "Jumlah Destinasi per Paket",
    "count": "Jumlah",
    "users": "Jumlah Pengguna",
    "interactions": "Jumlah Interaksi Rating",
    "avg_rating": "Rating Rata-rata",
    "err_rating": "Galat Baku Rating",
    "label": "Destinasi",
    "value": "Nilai",
    "variable": "Jenis",
    "Price_Tier": "Tier Harga",
}


def localize_chart(fig):
    """Translate technical dataframe column names shown by Plotly."""
    for axis_name in ("xaxis", "yaxis", "xaxis2", "yaxis2"):
        axis = getattr(fig.layout, axis_name, None)
        if axis and axis.title and axis.title.text in CHART_LABELS:
            axis.title.text = CHART_LABELS[axis.title.text]

    coloraxis = getattr(fig.layout, "coloraxis", None)
    if coloraxis and coloraxis.colorbar and coloraxis.colorbar.title:
        title = coloraxis.colorbar.title.text
        if title in CHART_LABELS:
            coloraxis.colorbar.title.text = CHART_LABELS[title]

    for trace in fig.data:
        if trace.hovertemplate:
            hovertemplate = trace.hovertemplate
            for source, translated in CHART_LABELS.items():
                hovertemplate = hovertemplate.replace(f"{source}=", f"{translated}: ")
            trace.hovertemplate = hovertemplate
        if trace.name in CHART_LABELS:
            trace.name = CHART_LABELS[trace.name]
    return fig


def protect_outside_bar_labels(fig):
    """Reserve plot space so labels outside bars remain fully visible."""
    horizontal_values = []
    vertical_values = []

    for trace in fig.data:
        if trace.type != "bar":
            continue

        positions = trace.textposition
        if isinstance(positions, str):
            has_outside_label = positions == "outside"
        else:
            has_outside_label = positions is not None and "outside" in positions
        if not has_outside_label:
            continue

        trace.update(cliponaxis=False)
        values = trace.x if trace.orientation == "h" else trace.y
        numeric_values = pd.to_numeric(pd.Series(values), errors="coerce").dropna()
        if trace.orientation == "h":
            horizontal_values.extend(numeric_values.tolist())
        else:
            vertical_values.extend(numeric_values.tolist())

    if horizontal_values:
        maximum = max(horizontal_values)
        current_range = fig.layout.xaxis.range
        desired_maximum = maximum * 1.38
        if current_range is None or current_range[1] < desired_maximum:
            fig.update_xaxes(range=[min(0, min(horizontal_values)), desired_maximum])

    if vertical_values:
        maximum = max(vertical_values)
        current_range = fig.layout.yaxis.range
        desired_maximum = maximum * 1.20
        if current_range is None or current_range[1] < desired_maximum:
            fig.update_yaxes(range=[min(0, min(vertical_values)), desired_maximum])

    return fig


def chart_layout(fig, height=420):
    fig = localize_chart(fig)
    fig = protect_outside_bar_labels(fig)
    has_legend = fig.layout.showlegend is not False and any(
        trace.showlegend is not False and trace.name not in (None, "")
        for trace in fig.data
    )
    chart_height = height
    bottom_margin = 115 if has_legend else 55

    fig.update_layout(
        height=chart_height,
        margin=dict(t=72, r=35, b=bottom_margin, l=55, autoexpand=True),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, Inter, Arial", color="#526C84", size=12),
        colorway=CHART_PALETTE,
        legend_title_text="",
        hoverlabel=dict(bgcolor="white", bordercolor="#D7E7F2", font_size=12),
        title_font=dict(family="Manrope, Arial", size=17, color="#123E73"),
        title_x=0.03,
        xaxis=dict(gridcolor="#EAF1F6", zerolinecolor="#E1EBF2", linecolor="#D7E4ED", automargin=True),
        yaxis=dict(gridcolor="#EAF1F6", zerolinecolor="#E1EBF2", linecolor="#D7E4ED", automargin=True),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(color="#405B73"),
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
        ),
        transition=dict(duration=280),
    )
    for trace in fig.data:
        if trace.type == "bar":
            trace.update(marker_line_width=0, marker_cornerradius=7, opacity=0.95)
        elif trace.type == "pie":
            trace.update(marker_line=dict(width=2, color="white"), pull=0)
    return fig


def show_chart(fig, height=420):
    fig = chart_layout(fig, height=height)
    fig.update_layout(autosize=True)
    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False, "responsive": True},
    )


def ranking_chart(data, label, value, title, color=COLORS["primary"], show_average=False):
    ranked = data.nlargest(10, value).sort_values(value).copy()
    axis_max = float(ranked[value].max()) * 1.20
    
    if show_average:
        avg_val = data[value].mean()
        ranked["Status"] = ["Di atas rata-rata" if v >= avg_val else "Di bawah rata-rata" for v in ranked[value]]
        color_map = {"Di atas rata-rata": color, "Di bawah rata-rata": "#9CC4E2"}
        
        fig = px.bar(
            ranked,
            x=value,
            y=label,
            orientation="h",
            title=title,
            text_auto=".2s",
            color="Status",
            color_discrete_map=color_map,
            labels=CHART_LABELS,
        )
        fig.add_vline(
            x=avg_val,
            line_dash="dash",
            line_color="#E74C3C",
            line_width=2,
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
    else:
        fig = px.bar(
            ranked,
            x=value,
            y=label,
            orientation="h",
            title=title,
            text_auto=".2s",
            labels=CHART_LABELS,
        )
        fig.update_traces(marker_color=color, textposition="outside", cliponaxis=False)

    fig.update_xaxes(range=[0, axis_max])
        
    return fig


def metric_row(items):
    columns = st.columns(len(items))
    for column, (label, value, helper, icon) in zip(columns, items):
        with column:
            metric_card(label, value, helper, icon)


def add_price_tier(data):
    data = data.copy()
    data["Price_Tier"] = pd.cut(
        data["Price"],
        bins=[-1, 0, 25_000, 75_000, 300_000, float("inf")],
        labels=PRICE_TIER_ORDER,
    )
    return data


datasets = load_datasets()
options = get_filter_options(datasets)
page, filters = render_app_sidebar(options, PAGES, PAGE_LABELS)
places, ratings, users, packages = apply_filters(datasets, filters)
analytics = build_analytics(places, ratings, users, packages)

if places.empty:
    render_empty_state()
    st.stop()

if ratings.empty:
    st.warning("Tidak ada interaksi rating untuk kelompok usia yang dipilih. Tambahkan kelompok usia agar analisis dapat ditampilkan.")
    st.stop()

if page == "Dashboard Overview":
    page_header(
        "Dashboard Overview",
        "Gambaran umum portofolio destinasi dan volume interaksi rating pada data aktif.",
        "OVERVIEW PARIWISATA",
    )

    metric_row([
        ("Total Destinasi", f"{len(places):,.0f}", "Lokasi wisata", "D"),
        ("Total Kota", f'{places["City"].nunique():,.0f}', "Cakupan kota", "K"),
        ("Total Kategori", f'{places["Category"].nunique():,.0f}', "Tipe wisata", "C"),
        ("Total Pengguna", f'{users["User_Id"].nunique():,.0f}', "Profil aktif", "U"),
        ("Interaksi Rating Unik", f"{len(ratings):,.0f}", "Pasangan pengguna-destinasi", "R"),
        ("Total Paket", f'{packages["Package"].nunique():,.0f}', "Paket tersedia", "P"),
    ])
    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

    category_distribution = (
        places.groupby("Category", as_index=False)
        .agg(destinations=("Place_Id", "nunique"))
        .sort_values("destinations", ascending=False)
    )
    city_distribution = (
        places.groupby("City", as_index=False)
        .agg(destinations=("Place_Id", "nunique"))
        .sort_values("destinations", ascending=False)
    )
    city_interactions = (
        ratings.groupby("City", as_index=False)
        .agg(interactions=("Rating_Observations", "sum"))
        .sort_values("interactions", ascending=False)
    )

    left, right = st.columns(2)
    with left:
        fig = px.pie(
            category_distribution,
            names="Category",
            values="destinations",
            hole=0.48,
            title="Distribusi Destinasi per Kategori",
            color="Category",
            color_discrete_map=CATEGORY_COLORS,
        )
        fig.update_traces(
            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>Jumlah destinasi: %{value}<br>Proporsi: %{percent}<extra></extra>",
        )
        show_chart(fig, height=460)

    with right:
        fig = ranking_chart(
            city_distribution,
            "City",
            "destinations",
            "Kota dengan Destinasi Terbanyak",
            show_average=True,
        )
        fig.update_layout(showlegend=True)
        show_chart(fig, height=460)

    fig = px.bar(
        city_interactions,
        x="City",
        y="interactions",
        title="Volume Interaksi Rating Wisatawan per Kota",
        text="interactions",
        color="City",
        color_discrete_map=CITY_COLORS,
        labels={"City": "Kota", "interactions": "Total Rating Diberikan"},
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition="outside")
    show_chart(fig, height=470)

    destination_map = analytics["destination"].copy()
    fig = px.scatter_map(
        destination_map,
        lat="Lat",
        lon="Long",
        color="Category",
        color_discrete_map=CATEGORY_COLORS,
        size="review_count",
        size_max=18,
        hover_name="Place_Name",
        hover_data={
            "Lat": False,
            "Long": False,
            "City": True,
            "Category": True,
            "Price": ":,",
            "user_rating": ":.2f",
            "review_count": True,
        },
        title="Peta Sebaran Destinasi",
        zoom=5.2,
        center={"lat": -7.2, "lon": 109.8},
        map_style="open-street-map",
        height=570,
    )
    fig.update_traces(cluster=dict(enabled=True))
    show_chart(fig, height=570)

    actionable = build_actionable_summary(analytics, ratings)
    section_header(
        "Prioritas & Tindakan BPPI",
        "",
    )

    status_colors = {
        "Kandidat Promosi Utama": "#174A7E",
        "Kandidat Promosi Niche": "#4E83B6",
        "Potensi Pengembangan": "#6E9FAD",
        "Perlu Validasi": "#C65364",
        "Monitor": "#AFC6D6",
    }
    fig = px.bar(
        actionable["status_counts"],
        x="Jumlah Destinasi",
        y="Status Promosi",
        orientation="h",
        color="Status Promosi",
        color_discrete_map=status_colors,
        text="Jumlah Destinasi",
        title="Distribusi Status Prioritas",
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition="outside")
    show_chart(fig, height=470)

    st.markdown("#### Daftar Tindakan Prioritas")
    status_options = actionable["status_counts"]["Status Promosi"].tolist()
    selected_statuses = st.multiselect(
        "Filter Status Prioritas",
        status_options,
        default=["Kandidat Promosi Utama", "Perlu Validasi"],
        key="priority_status_filter",
    )
    selected_statuses = selected_statuses or status_options
    priority_list = actionable["destinations"][
        actionable["destinations"]["Status Promosi"].isin(selected_statuses)
    ].sort_values(
        ["Skor Bukti", "user_rating", "review_count"],
        ascending=False,
    )
    st.caption(
        f"Menampilkan {len(priority_list):,} dari {len(actionable['destinations']):,} destinasi "
        f"untuk {len(selected_statuses)} status terpilih."
    )
    st.dataframe(
        priority_list,
        width="stretch",
        hide_index=True,
        column_order=[
            "Place_Name",
            "City",
            "Status Promosi",
            "user_rating",
            "review_count",
            "Tindakan BPPI",
        ],
        column_config={
            "Place_Name": st.column_config.TextColumn("Destinasi"),
            "City": st.column_config.TextColumn("Kota"),
            "Status Promosi": st.column_config.TextColumn("Status"),
            "user_rating": st.column_config.NumberColumn("Rating Pengguna", format="%.2f"),
            "review_count": st.column_config.NumberColumn("Interaksi Unik"),
            "Tindakan BPPI": st.column_config.TextColumn("Rekomendasi Tindakan"),
        },
    )

elif page == "Destinasi & Kategori":
    page_header(
        "Destinasi & Kategori",
        "",
        "ANALISIS DESTINASI",
    )

    user_by_category = (
        ratings.groupby("Category", as_index=False)
        .agg(
            user_rating=("Place_Ratings", "mean"),
            interactions=("Rating_Observations", "sum"),
        )
        .sort_values("user_rating", ascending=True)
    )

    fig = px.bar(
        user_by_category,
        x="user_rating",
        y="Category",
        orientation="h",
        title="Rating Pengguna Rata-rata per Kategori",
        text="user_rating",
        color="Category",
        color_discrete_map=CATEGORY_COLORS,
        custom_data=["interactions"],
        labels={"user_rating": "Rating Pengguna", "Category": "Kategori"},
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Rating pengguna: %{x:.2f}<br>Observasi rating: %{customdata[0]:,.0f}<extra></extra>",
    )
    show_chart(fig, height=470)

    age_rating = (
        ratings.groupby("Age_Group", observed=True)
        .agg(
            avg_rating=("Place_Ratings", "mean"),
            total_interaksi=("Place_Ratings", "count"),
            pct_tinggi=("Place_Ratings", lambda x: (x >= 4).mean() * 100),
        )
        .reset_index()
    )
    age_rating["Age_Group"] = age_rating["Age_Group"].astype(str)
    fig = px.line(
        age_rating,
        x="Age_Group",
        y="avg_rating",
        markers=True,
        title="Tren Rating Pengguna Berdasarkan Kelompok Usia",
        labels={"Age_Group": "Kelompok Usia", "avg_rating": "Rating Rata-rata"},
        custom_data=["total_interaksi", "pct_tinggi"],
    )
    fig.update_traces(
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=11, color=COLORS["primary"]),
        hovertemplate=(
            "<b>Usia %{x}</b><br>Rating rata-rata: %{y:.2f}"
            "<br>Total interaksi: %{customdata[0]:,}"
            "<br>Rating tinggi (≥4): %{customdata[1]:.1f}%<extra></extra>"
        ),
    )
    show_chart(fig, height=420)

    price_data = add_price_tier(places[["Place_Id", "Category", "Price"]])
    price_structure = (
        price_data.groupby(["Category", "Price_Tier"], observed=True)
        .agg(destinations=("Place_Id", "nunique"))
        .reset_index()
    )
    fig = px.bar(
        price_structure,
        x="Category",
        y="destinations",
        color="Price_Tier",
        category_orders={"Price_Tier": PRICE_TIER_ORDER},
        color_discrete_map=PRICE_TIER_COLORS,
        title="Struktur Harga per Kategori",
        labels={"Category": "Kategori", "destinations": "Jumlah Destinasi", "Price_Tier": "Tier Harga"},
        custom_data=["Price_Tier"],
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{customdata[0]}: %{y} destinasi<extra></extra>"
    )
    show_chart(fig, height=500)

    top_destinations = analytics["top_rated"].head(10).sort_values(
        ["user_rating", "review_count", "Place_Name"],
        ascending=[False, False, True],
    ).copy()
    destination_order = top_destinations["Place_Name"].tolist()
    fig = px.bar(
        top_destinations,
        x="user_rating",
        y="Place_Name",
        orientation="h",
        title="Top 10 Destinasi Berdasarkan Rating Pengguna",
        text="user_rating",
        color="Category",
        color_discrete_map=CATEGORY_COLORS,
        category_orders={"Place_Name": destination_order},
        custom_data=["Category", "City", "review_count"],
        labels={"user_rating": "Rating Pengguna", "Place_Name": "Destinasi"},
    )
    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>Kategori: %{customdata[0]}<br>Kota: %{customdata[1]}"
            "<br>Rating pengguna: %{x:.2f}<br>Interaksi unik: %{customdata[2]:,.0f}<extra></extra>"
        ),
    )
    fig.update_yaxes(categoryorder="array", categoryarray=destination_order[::-1])
    show_chart(fig, height=560)

elif page == "Paket & Harga":
    page_header(
        "Paket & Harga",
        "",
        "ANALISIS HARGA",
    )

    average_price = (
        places.groupby("Category", as_index=False)
        .agg(avg_price=("Price", "mean"))
        .sort_values("avg_price", ascending=True)
    )
    price_tiers = add_price_tier(places[["Place_Id", "Price"]])
    tier_distribution = (
        price_tiers.groupby("Price_Tier", observed=False)
        .agg(destinations=("Place_Id", "nunique"))
        .reindex(PRICE_TIER_ORDER, fill_value=0)
        .reset_index()
    )
    tier_distribution["Legend"] = (
        tier_distribution["Price_Tier"].astype(str)
        + " "
        + tier_distribution["destinations"].astype(str)
    )

    left, right = st.columns(2)
    with left:
        average_price["label"] = average_price["avg_price"].map(lambda value: f"Rp {value:,.0f}")
        fig = px.bar(
            average_price,
            x="avg_price",
            y="Category",
            orientation="h",
            title="Harga Rata-rata Tiket per Kategori (Rp)",
            text="label",
            color="Category",
            color_discrete_map=CATEGORY_COLORS,
            labels={"avg_price": "Harga Rata-rata (Rp)", "Category": "Kategori"},
        )
        fig.update_layout(showlegend=False)
        fig.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Harga rata-rata tiket: Rp %{x:,.0f}<extra></extra>",
        )
        fig.update_xaxes(tickprefix="Rp ", separatethousands=True)
        show_chart(fig, height=500)

    with right:
        fig = px.pie(
            tier_distribution,
            names="Legend",
            values="destinations",
            hole=0.48,
            title="Distribusi Tier Harga Keseluruhan Destinasi",
            color="Price_Tier",
            color_discrete_map=PRICE_TIER_COLORS,
            category_orders={"Price_Tier": PRICE_TIER_ORDER},
            custom_data=["Price_Tier", "destinations"],
        )
        fig.update_traces(
            textinfo="percent",
            hovertemplate="<b>%{customdata[0]}</b><br>Jumlah destinasi: %{customdata[1]}<br>Proporsi: %{percent}<extra></extra>",
        )
        show_chart(fig, height=500)

    tier_rating = ratings.merge(
        add_price_tier(places[["Place_Id", "Price"]])[["Place_Id", "Price_Tier"]],
        on="Place_Id",
        how="left",
    )
    tier_trend = (
        tier_rating.groupby("Price_Tier", observed=True)
        .agg(
            avg_rating=("Place_Ratings", "mean"),
            total_interaksi=("Place_Ratings", "count"),
            pct_tinggi=("Place_Ratings", lambda x: (x >= 4).mean() * 100),
        )
        .reindex(PRICE_TIER_ORDER)
        .reset_index()
    )
    fig = px.line(
        tier_trend,
        x="Price_Tier",
        y="avg_rating",
        markers=True,
        title="Tren Harga Tiket dari Tier Terjangkau hingga Premium",
        labels={"Price_Tier": "Tier Harga", "avg_rating": "Rating Rata-rata Pengguna"},
        custom_data=["total_interaksi", "pct_tinggi"],
    )
    fig.update_traces(
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=11, color=COLORS["primary"]),
        hovertemplate=(
            "<b>%{x}</b><br>Rating rata-rata: %{y:.2f}"
            "<br>Total interaksi: %{customdata[0]:,}"
            "<br>Rating tinggi (≥4): %{customdata[1]:.1f}%<extra></extra>"
        ),
    )
    show_chart(fig, height=420)


render_footer()
