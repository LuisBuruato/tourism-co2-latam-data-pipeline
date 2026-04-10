import pandas as pd
import os

# =========================
# PATHS (DOCKER)
# =========================

INPUT_PATH = "/opt/airflow/data/silver/silver_integrated.parquet"
OUTPUT_PATH = "/opt/airflow/data/gold/kpis_country.parquet"

# =========================
# LOAD
# =========================

def load_data():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError("No existe silver dataset")

    return pd.read_parquet(INPUT_PATH)

# =========================
# KPIs
# =========================

def create_kpis(df):
    print("📊 Calculando KPIs...")

    df = df.sort_values(["country_code", "year"])

    # Growth metrics
    df["tourism_growth"] = df.groupby("country_code")["tourism_arrivals"].pct_change()
    df["co2_growth"] = df.groupby("country_code")["co2"].pct_change()

    # Decoupling index
    df["decoupling_index"] = df["co2_growth"] - df["tourism_growth"]

    return df

# =========================
# SAVE
# =========================

def save_data(df):
    os.makedirs("/opt/airflow/data/gold", exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print(f"✅ GOLD guardado en: {OUTPUT_PATH}")

# =========================
# MAIN
# =========================

def main():
    print("🚀 Generando capa GOLD...\n")

    df = load_data()
    df = create_kpis(df)
    save_data(df)

    print("\n🎉 KPIs listos para análisis")

# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()