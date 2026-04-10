import pandas as pd

# =========================
# PATHS (DOCKER READY)
# =========================

RAW_PATH = "/opt/airflow/data/raw/tourism_co2_latam_raw.csv"
CO2_PATH = "/opt/airflow/data/silver/co2_latam_clean.parquet"
OUTPUT_PATH = "/opt/airflow/data/silver/silver_integrated.parquet"

# =========================
# MAIN
# =========================

def integrate_data():
    print("🧠 Integrando datasets...")

    # =========================
    # LOAD DATA
    # =========================

    raw = pd.read_csv(RAW_PATH)
    co2 = pd.read_parquet(CO2_PATH)

    # =========================
    # CLEAN RAW
    # =========================

    raw = raw.rename(columns={
        "country": "country_code"
    })

    raw["year"] = pd.to_numeric(raw["year"], errors="coerce")
    raw = raw.dropna(subset=["year"])
    raw["year"] = raw["year"].astype(int)

    # =========================
    # CLEAN CO2
    # =========================

    co2["year"] = co2["year"].astype(int)
    co2["country_code"] = co2["country_code"].astype(str)

    # =========================
    # MERGE
    # =========================

    df = raw.merge(co2, on=["country_code", "year"], how="inner")

    # =========================
    # FILTER LATAM YEARS
    # =========================

    df = df[df["year"].between(2013, 2023)]

    # =========================
    # FEATURE ENGINEERING
    # =========================

    df["co2_per_tourist"] = df["co2"] / df["tourism_arrivals"]
    df["co2_per_gdp"] = df["co2"] / df["gdp"]

    # =========================
    # SORT
    # =========================

    df = df.sort_values(["country_code", "year"])

    # =========================
    # SAVE
    # =========================

    df.to_parquet(OUTPUT_PATH, index=False)

    print("✅ Silver integrado creado")
    print(df.head())


# =========================
# RUN
# =========================

if __name__ == "__main__":
    integrate_data()