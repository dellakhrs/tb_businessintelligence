import streamlit as st

COLORS = {
    "primary": "#174A7E",
    "secondary": "#4E83B6",
    "accent": "#A8CBE8",
    "light": "#EAF4FC",
    "danger": "#C65364",
}


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
        *{box-sizing:border-box}html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:#17324D}
        html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{max-width:100%;overflow-x:hidden!important}
        .stApp{background:radial-gradient(circle at 88% 4%,#DDECF8 0,transparent 25%),linear-gradient(180deg,#F3F8FC,#FAFCFE 48%,#EDF6FC)}
        header[data-testid="stHeader"]{background:transparent!important}[data-testid="stDecoration"],#MainMenu,footer{display:none!important}
        .block-container{padding:2rem 1.5rem 2rem;max-width:none!important;width:100%!important;margin:0!important;overflow-x:hidden}
        div[data-testid="stHorizontalBlock"],
        div[data-testid="stHorizontalBlock"]>div[data-testid="column"],
        div[data-testid="stVerticalBlock"],
        div[data-testid="stElementContainer"]{min-width:0!important;max-width:100%!important}
        section[data-testid="stSidebar"],section[data-testid="stSidebar"]>div:first-child{width:280px!important;min-width:280px!important;max-width:280px!important}
        section[data-testid="stSidebar"]{background:linear-gradient(180deg,#F0F7FC,#E0EFF9)!important;border-right:1px solid #C8DEEC!important}
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"]{display:none!important;height:0!important;min-height:0!important;padding:0!important;margin:0!important}
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding:0!important;margin:0!important}
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding:.45rem .75rem 1rem!important;margin:0!important;width:100%!important;max-width:100%!important}
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]>div[data-testid="stVerticalBlock"]{gap:.4rem!important;width:100%!important}
        [data-testid="stSidebarContent"]>div,
        [data-testid="stSidebarContent"] [data-testid="stVerticalBlock"],
        [data-testid="stSidebarContent"] [data-testid="stElementContainer"],
        [data-testid="stSidebarUserContent"]>div,
        [data-testid="stSidebarUserContent"] [data-testid="stElementContainer"]{width:100%!important;max-width:100%!important;min-width:0!important}
        section[data-testid="stSidebar"] [data-testid="stImage"]{width:100%!important;margin:0!important;padding:0!important}
        section[data-testid="stSidebar"] [data-testid="stImage"] img{display:block!important;width:100%!important;height:auto!important;margin:0!important;object-fit:contain!important}
        .sidebar-brand{display:block;width:100%;margin:0 0 .1rem;padding:0}
        .sidebar-brand img{display:block;width:100%;height:auto;margin:0 0 .3rem;object-fit:contain}
        .sidebar-menu-label{margin:.2rem 0 .1rem;padding:0 3px;color:#6686A2;font-size:.66rem;font-weight:800;letter-spacing:.8px;text-transform:uppercase}
        .filter-selection-status{margin:-.15rem 0 .2rem;color:#6686A2;font-size:.66rem;font-weight:600}
        [data-testid="stSidebar"] [data-testid="stRadio"]>label[data-testid="stWidgetLabel"]{display:none!important}
        [data-testid="stSidebar"] [data-testid="stRadio"],
        [data-testid="stSidebar"] [data-testid="stRadio"]>div,
        [data-testid="stSidebar"] [data-testid="stRadio"]>div>div,
        [data-testid="stSidebar"] [role="radiogroup"]{width:100%!important;max-width:100%!important}
        [data-testid="stSidebar"] [role="radiogroup"]{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:4px!important}
        [data-testid="stSidebar"] [role="radiogroup"]>label,
        [data-testid="stSidebar"] label[data-baseweb="radio"]{display:flex!important;align-items:center!important;width:100%!important;max-width:none!important;height:42px!important;min-height:42px!important;margin:0!important;padding:0 12px!important;border-radius:11px!important;cursor:pointer!important;transition:.2s!important}
        [data-testid="stSidebar"] label[data-baseweb="radio"]>div:first-child{display:none!important}
        [data-testid="stSidebar"] label[data-baseweb="radio"]>div:last-child{width:100%!important}
        [data-testid="stSidebar"] label[data-baseweb="radio"] p{margin:0!important;color:#385873!important;font-size:.79rem!important;font-weight:600!important;white-space:nowrap!important}
        [data-testid="stSidebar"] label[data-baseweb="radio"]:hover{background:rgba(255,255,255,.75)!important}
        [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked){background:linear-gradient(135deg,#3974B0,#24558F)!important;box-shadow:0 7px 16px rgba(36,85,143,.2)!important}
        [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p{color:#fff!important}
        [data-testid="stSidebar"] hr{width:100%!important;border-color:#BBD5E8!important;margin:.75rem 0!important}
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{font-size:.72rem!important;font-weight:700!important;color:#426787!important}
        [data-testid="stSidebar"] [data-baseweb="select"]>div{min-height:42px!important;background:#fff!important;border-color:#BED7E9!important;border-radius:11px!important}
        [data-testid="stSidebar"] [data-baseweb="select"],
        [data-testid="stSidebar"] [data-testid="stSlider"],
        [data-testid="stSidebar"] [data-testid="stButton"]{width:100%!important;max-width:100%!important}
        [data-testid="stSidebar"] [data-baseweb="tag"]{background:#1E4F8A!important;border-radius:999px!important}
        [data-testid="stSidebar"] [data-baseweb="tag"] *{color:#fff!important;fill:#fff!important}
        [data-testid="stSidebar"] .stButton>button{width:100%;min-height:43px;border-radius:11px;border:1px solid #BBD4E6;color:#174A7E;font-weight:700;background:#fff}
        .page-hero{position:relative;overflow:hidden;border-radius:24px;padding:30px 34px;margin-bottom:26px;min-height:190px;display:flex;flex-direction:column;justify-content:center;background-color:#123E73;background-size:cover;background-position:center 55%;box-shadow:0 18px 50px rgba(18,62,115,.2)}
        .page-hero:after{content:"";position:absolute;width:250px;height:250px;border-radius:50%;right:-55px;top:-145px;background:rgba(255,255,255,.07)}
        .page-hero>div{position:relative;z-index:1}
        .eyebrow{font-size:.68rem;font-weight:800;letter-spacing:1.7px;color:#C5E0F3}.page-title{font:800 2.4rem Manrope;color:#fff;margin:7px 0;letter-spacing:-1px}.page-subtitle{font-size:.92rem;color:#DCECF7}
        .section-head{margin:14px 2px 14px}.section-line{width:43px;height:4px;background:linear-gradient(90deg,#174A7E,#75AED4);border-radius:5px;margin-bottom:8px}.section-head strong{font:800 1.12rem Manrope;color:#173F68}.section-head span{display:block;font-size:.76rem;color:#7E99B1;margin-top:4px}
        .metric-box{position:relative;overflow:hidden;min-height:170px;padding:21px;border-radius:20px;background:linear-gradient(145deg,#fff,#F7FBFE);border:1px solid #D8E8F4;box-shadow:0 13px 34px rgba(30,79,117,.08);transition:.2s}
        .metric-box:hover{transform:translateY(-3px);box-shadow:0 17px 38px rgba(30,79,117,.13)}
        .metric-icon{width:37px;height:37px;border-radius:11px;display:grid;place-items:center;margin-bottom:13px;background:linear-gradient(145deg,#EDF6FC,#DCECF8);border:1px solid #D2E6F4;color:#174A7E}
        .metric-icon svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
        .metric-label{font-size:.7rem;color:#6F8DA7;font-weight:700;text-transform:uppercase;letter-spacing:.7px}.metric-value{font:800 1.55rem Manrope;color:#174A7E;margin:11px 0 4px}.metric-help{font-size:.72rem;color:#8BA4B9}
        .kpi-status{min-height:185px;padding:20px;border-radius:20px;background:#fff;border:1px solid #D8E8F4;box-shadow:0 13px 34px rgba(30,79,117,.08)}
        .kpi-status-top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}.kpi-status-label{color:#6F8DA7;font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.6px}
        .kpi-status-value{font:800 1.7rem Manrope;color:#173F68;margin:15px 0 5px}.kpi-status-target{font-size:.72rem;color:#718CA4}.kpi-status-action{font-size:.72rem;line-height:1.45;color:#56738C;margin-top:13px}
        .status-pill{white-space:nowrap;border-radius:999px;padding:5px 9px;font-size:.62rem;font-weight:800}.status-good{background:#E3F5EA;color:#237A4B}.status-watch{background:#FFF2D9;color:#A56300}.status-critical{background:#FBE4E7;color:#B23A4A}
        .alert-banner{display:flex;align-items:center;gap:16px;padding:18px 20px;border-radius:18px;background:linear-gradient(100deg,#FFF7F1,#FFF);border:1px solid #F4D5C3;border-left:5px solid #D76A45;box-shadow:0 10px 28px rgba(133,75,48,.08)}
        .alert-count{font:800 1.8rem Manrope;color:#B54E31}.alert-copy strong{display:block;color:#7D3827;font:800 .9rem Manrope;margin-bottom:3px}.alert-copy span{color:#8C655A;font-size:.75rem}
        div[data-testid="stPlotlyChart"]{background:rgba(255,255,255,.95);border:1px solid #DCEAF4;border-radius:22px;overflow:visible!important;box-shadow:0 14px 38px rgba(29,75,110,.08);padding:0;width:100%!important;max-width:100%!important;min-width:0!important}
        div[data-testid="stPlotlyChart"]>div,
        div[data-testid="stPlotlyChart"] .js-plotly-plot,
        div[data-testid="stPlotlyChart"] .plot-container,
        div[data-testid="stPlotlyChart"] .user-select-none,
        div[data-testid="stPlotlyChart"] .svg-container,
        div[data-testid="stPlotlyChart"] svg,
        div[data-testid="stPlotlyChart"] iframe{width:100%!important;max-width:100%!important;min-width:0!important}
        div[data-testid="stDataFrame"]{background:rgba(255,255,255,.95);border:1px solid #DCEAF4;border-radius:22px;overflow-x:auto;box-shadow:0 14px 38px rgba(29,75,110,.08);padding:10px;width:100%}
        .highlight-card{background:#fff;border:1px solid #DCEAF4;border-radius:20px;padding:20px 22px;box-shadow:0 12px 30px rgba(29,75,110,.07);min-height:118px;display:flex;gap:15px;align-items:center}
        .highlight-icon{width:54px;height:54px;min-width:54px;border-radius:50%;display:grid;place-items:center;background:#E5F1F9;color:#174A7E;border:1px solid #D1E4F1}.highlight-icon svg{width:26px;height:26px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
        .highlight-label{font-size:.67rem;color:#7892A9;text-transform:uppercase;font-weight:800}.highlight-value{font:800 .94rem Manrope;color:#123E73;margin:4px 0}.highlight-help{font-size:.7rem;color:#8299AD}
        .note-card{background:linear-gradient(135deg,#174A7E,#286A9E);border-radius:17px;padding:18px 20px;height:100%;box-shadow:0 14px 30px rgba(18,62,115,.17)}.note-card strong{display:block;color:#fff;font:700 .88rem Manrope;margin-bottom:6px}.note-card span{color:#CFE4F3;font-size:.78rem;line-height:1.55}
        .insight-box{background:linear-gradient(100deg,#fff,#F1F8FD);border:1px solid #D7E8F4;border-top:3px solid #4E83B6;border-radius:18px;padding:16px 19px;margin:11px 0}.insight-box strong{font-family:Manrope;color:#174A7E}.insight-box span{color:#57738D;font-size:.9rem}
        .footer{text-align:center;color:#7997B2;font-size:.72rem;margin-top:28px}
        h1,h2,h3{font-family:Manrope,sans-serif!important;color:#173F68!important}
        @media(max-width:1000px){
            div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) {
                display:flex!important;
                flex-direction:column!important;
                gap:1.5rem!important;
            }
            div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPlotlyChart"]) > div[data-testid="column"] {
                width:100%!important;
                min-width:100%!important;
                max-width:100%!important;
            }
            section[data-testid="stSidebar"],section[data-testid="stSidebar"]>div:first-child{width:260px!important;min-width:260px!important;max-width:260px!important}
            .block-container{padding:2rem 1rem}.page-title{font-size:1.8rem}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _icon_svg(name: str) -> str:
    icons = {
        "explore": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2.1 4.9-4.9 2.1 2.1-4.9 4.9-2.1Z"/>',
        "location_city": '<path d="M4 21V7h7v14M11 11h9v10M7 10h1M7 14h1M7 18h1M14 14h1M14 18h1M18 14h1M18 18h1M2 21h20"/>',
        "category": '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
        "group": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
        "reviews": '<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4v8Z"/><path d="m12 7 1.2 2.4 2.8.4-2 2 .5 2.7-2.5-1.3-2.5 1.3.5-2.7-2-2 2.8-.4L12 7Z"/>',
        "luggage": '<path d="M8 7V5a3 3 0 0 1 3-3h2a3 3 0 0 1 3 3v2M6 7h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2ZM9 11v6M15 11v6"/>',
        "schedule": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "groups": '<path d="M16 20v-1a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v1M8.5 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM23 20v-1a4 4 0 0 0-3-3.9"/>',
        "location_on": '<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        "workspace_premium": '<circle cx="12" cy="9" r="6"/><path d="m8 14-1 8 5-3 5 3-1-8"/>',
        "warning": '<path d="M10.3 3.6 2.2 18a2 2 0 0 0 1.8 3h16a2 2 0 0 0 1.8-3L13.7 3.6a2 2 0 0 0-3.4 0ZM12 9v4M12 17h.01"/>',
        "payments": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>',
        "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3Z"/>',
    }
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{icons.get(name, icons["star"])}</svg>'


def page_header(title: str, subtitle: str, eyebrow: str) -> None:
    background = (
        "linear-gradient(90deg, rgba(8,31,55,.62) 0%, rgba(10,35,58,.24) 48%, "
        "rgba(10,35,58,.03) 100%), "
        "url('/app/static/tourism-hero.png')"
    )
    st.markdown(
        f'<div class="page-hero" style="background-image:{background}">'
        f'<div class="eyebrow">{eyebrow}</div><div class="page-title">{title}</div>'
        f'<div class="page-subtitle">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, helper: str, icon: str = "star") -> None:
    icon_map = {"D": "explore", "K": "location_city", "C": "category", "U": "group", "R": "reviews", "P": "luggage", "A": "schedule", "S": "groups", "L": "location_on", "1": "workspace_premium", "!": "warning", "Rp": "payments", "★": "star"}
    st.markdown(f'<div class="metric-box"><div class="metric-icon">{_icon_svg(icon_map.get(icon, icon))}</div><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-help">{helper}</div></div>', unsafe_allow_html=True)


def kpi_status_card(label: str, value: str, target: str, status: str, action: str) -> None:
    status_class = {
        "Tercapai": "status-good",
        "Perlu Perhatian": "status-watch",
        "Kritis": "status-critical",
    }.get(status, "status-watch")
    st.markdown(
        f'<div class="kpi-status"><div class="kpi-status-top"><div class="kpi-status-label">{label}</div>'
        f'<span class="status-pill {status_class}">{status}</span></div><div class="kpi-status-value">{value}</div>'
        f'<div class="kpi-status-target">Target: {target}</div><div class="kpi-status-action">{action}</div></div>',
        unsafe_allow_html=True,
    )


def alert_banner(count: int, high_count: int) -> None:
    st.markdown(
        f'<div class="alert-banner"><div class="alert-count">{count}</div><div class="alert-copy">'
        f'<strong>Peringatan aktif membutuhkan tindak lanjut</strong><span>{high_count} prioritas tinggi. '
        'Gunakan Pusat Tindakan untuk melihat bukti, penanggung jawab, target waktu, dan KPI pemantauan.</span></div></div>',
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="section-head"><div class="section-line"></div><strong>{title}</strong><span>{subtitle}</span></div>', unsafe_allow_html=True)


def insight_card(title: str, text: str) -> None:
    st.markdown(f'<div class="insight-box"><strong>{title}</strong><br><span>{text}</span></div>', unsafe_allow_html=True)


def note_card(title: str, text: str) -> None:
    st.markdown(f'<div class="note-card"><strong>{title}</strong><span>{text}</span></div>', unsafe_allow_html=True)


def highlight_card(icon: str, label: str, value: str, helper: str) -> None:
    st.markdown(f'<div class="highlight-card"><div class="highlight-icon">{_icon_svg(icon)}</div><div><div class="highlight-label">{label}</div><div class="highlight-value">{value}</div><div class="highlight-help">{helper}</div></div></div>', unsafe_allow_html=True)


def render_app_sidebar(options: dict, pages: list[str], page_labels: dict[str, str]) -> tuple[str, dict]:
    defaults = {"filter_cities": options["cities"], "filter_category": "Semua Kategori", "filter_price": options["price"], "filter_rating": options["rating"], "filter_ages": options["ages"]}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    def reset_filters() -> None:
        for key, value in defaults.items():
            st.session_state[key] = value

    with st.sidebar:
        st.image("assets/logo_javista.png", width="stretch")
        st.markdown(
            '<div class="sidebar-menu-label">Menu Utama</div>',
            unsafe_allow_html=True,
        )
        page = st.radio("Navigasi", pages, format_func=lambda value: page_labels[value], label_visibility="collapsed", key="main_navigation")
        st.divider()
        st.markdown('<div class="sidebar-menu-label">Filter Analisis</div>', unsafe_allow_html=True)
        cities = st.multiselect(
            "Kota",
            options["cities"],
            key="filter_cities",
            placeholder="Pilih kota yang ingin dianalisis",
        )
        st.markdown(
            f'<div class="filter-selection-status">{len(cities)} dari {len(options["cities"])} kota dipilih</div>',
            unsafe_allow_html=True,
        )
        category = st.selectbox("Kategori Wisata", ["Semua Kategori", *options["categories"]], key="filter_category")
        price = st.slider("Rentang Harga Tiket", *options["price"], key="filter_price")
        rating = st.slider("Rentang Rating", *options["rating"], key="filter_rating")
        ages = st.multiselect(
            "Kelompok Usia",
            options["ages"],
            key="filter_ages",
            placeholder="Pilih kelompok usia",
        )
        st.markdown(
            f'<div class="filter-selection-status">{len(ages)} dari {len(options["ages"])} kelompok usia dipilih</div>',
            unsafe_allow_html=True,
        )
        st.button("Reset Filter", on_click=reset_filters, width="stretch")
    return page, {"cities": cities or options["cities"], "categories": options["categories"] if category == "Semua Kategori" else [category], "price": price, "rating": rating, "ages": ages or options["ages"]}


def render_empty_state() -> None:
    st.info("Tidak ada data yang sesuai dengan filter aktif. Silakan ubah filter pada sidebar.")


def render_footer() -> None:
    st.markdown('<div class="footer">© Dashboard BI BPPI - 2026</div>', unsafe_allow_html=True)
