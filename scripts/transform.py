import pandas as pd
import os

from extract_co2_owid import get_co2_data

# =========================
# CONFIG
# =========================

INPUT_PATH = "data/raw/tourism_co2_latam_raw.csv"
OUTPUT_PATH = "data/processed/tourism_co2_latam_clean.csv"


# =========================
# CREATE FOLDER
# =========================

def ensure_folders():
    os.makedirs("data/processed", exist_ok=True)


# =========================
# LOAD DATA
# =========================

def load_data():
    print("📥 Cargando datos raw...")
    df = pd.read_csv(INPUT_PATH)
    return df


# =========================
# CLEAN WORLD BANK DATA
# =========================

def clean_data(df):
    print("🧹 Limpiando datos...")

    # tipos
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # eliminar inválidos
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    # filtrar rango
    df = df[(df["year"] >= 2000) & (df["year"] <= 2023)]

    # ordenar
    df = df.sort_values(["country", "year"])

    # eliminar duplicados
    df = df.drop_duplicates(subset=["country", "year"])

    # eliminar nulos críticos
    df = df.dropna(subset=["tourism_arrivals", "gdp"])

    return df


# =========================
# MERGE CO2 (OWID)
# =========================

def merge_co2(df):
    print("🌫️ Integrando CO₂ (OWID)...")

    co2_df = get_co2_data()

    df = df.merge(co2_df, on=["country", "year"], how="left")

    return df


# =========================
# FEATURE ENGINEERING
# =========================

def create_features(df):
    print("🧠 Creando features...")

    # evitar división por cero
    df["tourism_arrivals"] = df["tourism_arrivals"].replace(0, pd.NA)
    df["gdp"] = df["gdp"].replace(0, pd.NA)

    # métricas clave
    df["co2_per_tourist"] = df["co2"] / df["tourism_arrivals"]
    df["co2_per_gdp"] = df["co2"] / df["gdp"]

    # crecimiento
    df["tourism_growth"] = df.groupby("country")["tourism_arrivals"].pct_change()
    df["co2_growth"] = df.groupby("country")["co2"].pct_change()

    # desacoplamiento
    df["decoupling_index"] = df["co2_growth"] - df["tourism_growth"]

    return df


# =========================
# FINAL CLEAN
# =========================

def finalize(df):
    print("✨ Ajustes finales...")

    # reemplazar infinitos
    df = df.replace([float("inf"), -float("inf")], pd.NA)

    # rellenar crecimiento inicial
    df["tourism_growth"] = df["tourism_growth"].fillna(0)
    df["co2_growth"] = df["co2_growth"].fillna(0)
    df["decoupling_index"] = df["decoupling_index"].fillna(0)

    return df


# =========================
# SAVE
# =========================

def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ Dataset limpio guardado en: {OUTPUT_PATH}")
    print("\n📊 Preview:")
    print(df.head())


# =========================
# MAIN
# =========================

def transform_all():
    ensure_folders()

    df = load_data()
    df = clean_data(df)
    df = merge_co2(df)
    df = create_features(df)
    df = finalize(df)

    save_data(df)

    return df


# =========================
# RUN
# =========================

if __name__ == "__main__":
    print("🔥 Ejecutando transform...\n")
    transform_all()