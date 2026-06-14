import streamlit as st


def render_kpis(domestic: int, international: int, revenue: float, occupancy: float) -> None:
    columns = st.columns(4)
    columns[0].metric("Wisatawan Domestik", f"{domestic:,.0f}")
    columns[1].metric("Wisatawan Mancanegara", f"{international:,.0f}")
    columns[2].metric("Pendapatan", f"Rp {revenue / 1_000_000_000:,.1f} M")
    columns[3].metric("Rata-rata Hunian Hotel", f"{occupancy:,.1f}%")

