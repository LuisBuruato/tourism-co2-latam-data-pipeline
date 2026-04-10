import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Tourism vs CO2 LATAM", layout="wide")

# =========================
# LOAD DATA (ROBUST PATH)
# =========================

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(BASE_DIR, "data", "gold", "kpis_country.parquet")
    return pd.read_parquet(path)

df = load_data()

# =========================
# TITLE
# =========================

st.title("🌎 Tourism vs CO₂ in LATAM")
st.markdown("Analyze sustainability trends across Latin America")

# =========================
# FILTERS
# =========================

countries = st.multiselect(
    "Select Countries",
    df["country_code"].unique(),
    default=["MEX", "BRA", "ARG"]
)

year_range = st.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (2015, 2023)
)

df_filtered = df[
    (df["country_code"].isin(countries)) &
    (df["year"].between(year_range[0], year_range[1]))
]

# =========================
# KPIs (TOP ROW)
# =========================

col1, col2, col3 = st.columns(3)

col1.metric("Total CO₂", f"{df_filtered['co2'].sum():,.0f}")
col2.metric("Total Tourists", f"{df_filtered['tourism_arrivals'].sum():,.0f}")
col3.metric("Avg Decoupling Index", f"{df_filtered['decoupling_index'].mean():.4f}")

# =========================
# LINE CHART CO2
# =========================

fig1 = px.line(
    df_filtered,
    x="year",
    y="co2",
    color="country_code",
    title="CO₂ Emissions Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# LINE CHART TOURISM
# =========================

fig2 = px.line(
    df_filtered,
    x="year",
    y="tourism_arrivals",
    color="country_code",
    title="Tourism Arrivals Over Time"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# SCATTER CORRELATION
# =========================

fig3 = px.scatter(
    df_filtered,
    x="tourism_arrivals",
    y="co2",
    color="country_code",
    size="gdp",
    hover_data=["year"],
    title="Tourism vs CO₂ Correlation"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# TOP COUNTRIES
# =========================

st.subheader("🌱 Most Sustainable Countries (Decoupling)")

top = (
    df.groupby("country_code")["decoupling_index"]
    .mean()
    .sort_values()
    .head(5)
    .reset_index()
)

st.dataframe(top)

# =========================
# RAW DATA
# =========================

with st.expander("📂 View Raw Data"):
    st.dataframe(df_filtered)