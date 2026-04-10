import pandas as pd
import os
import argparse
import logging

# =========================
# CONFIG
# =========================

INPUT_PATH = "/opt/airflow/data/raw/owid_co2/owid_co2_original.csv"
OUTPUT_BASE = "data/bronze/co2_emissions"

LATAM_ISO3 = [
    "ARG","BOL","BRA","CHL","COL","CRI","CUB","DOM","ECU",
    "SLV","GTM","HND","MEX","NIC","PAN","PRY","PER","URY","VEN"
]

START_YEAR = 2013
END_YEAR = 2023

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# MAIN
# =========================

def process(dry_run=False):
    logging.info("📥 Cargando OWID original...")

    # ✅ VALIDACIÓN INPUT
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"No existe archivo: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    # =========================
    # CLEAN + RENAME
    # =========================

    df = df.rename(columns={
        "iso_code": "country_code"
    })

    # =========================
    # FILTER LATAM + YEARS
    # =========================

    df = df[
        (df["country_code"].isin(LATAM_ISO3)) &
        (df["year"].between(START_YEAR, END_YEAR))
    ]

    # ✅ VALIDACIÓN DATASET
    if df.empty:
        raise ValueError("Dataset vacío después del filtrado")

    # =========================
    # LOGGING PRO
    # =========================

    logging.info(f"📊 Registros totales: {len(df)}")
    logging.info(f"🌎 Países encontrados: {df['country_code'].nunique()}")
    logging.info(f"📅 Rango años: {df['year'].min()} - {df['year'].max()}")

    # =========================
    # SELECT COLUMNS
    # =========================

    cols = ["country_code", "year", "co2"]
    df = df[cols].dropna()

    # =========================
    # TIPADO EXPLÍCITO
    # =========================

    df["year"] = df["year"].astype(int)
    df["country_code"] = df["country_code"].astype(str)

    # =========================
    # PARTITION WRITE
    # =========================

    partitions = 0

    for (year, country), group in df.groupby(["year", "country_code"]):

        path = f"{OUTPUT_BASE}/year={year}/country_code={country}"
        file_path = f"{path}/data.parquet"

        partitions += 1

        if dry_run:
            logging.info(f"[DRY RUN] → {file_path}")
        else:
            os.makedirs(path, exist_ok=True)

            group.to_parquet(
                file_path,
                index=False,
                compression="snappy"
            )

    # =========================
    # SUMMARY
    # =========================

    logging.info("✅ Proceso terminado")
    logging.info(f"📦 Particiones generadas: {partitions}")
    logging.info(f"🌎 Países cubiertos: {df['country_code'].nunique()}")

# =========================
# CLI
# =========================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Simula sin escribir archivos")

    args = parser.parse_args()

    process(dry_run=args.dry_run)