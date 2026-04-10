import pandas as pd
import os
import logging
import argparse

# =========================
# CONFIG
# =========================

INPUT_PATH = "data/raw/tourism_co2_latam_raw.csv"
OUTPUT_BASE = "data/bronze/tourism"

LATAM_ISO3 = [
    "ARG","BOL","BRA","CHL","COL","CRI","CUB","DOM","ECU",
    "SLV","GTM","HND","MEX","NIC","PAN","PRY","PER","URY","VEN"
]

START_YEAR = 2013
END_YEAR = 2023

# =========================
# LOGGING
# =========================

logging.basicConfig(level=logging.INFO)

# =========================
# MAIN
# =========================

def process(dry_run=False):

    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError("Archivo tourism raw no encontrado")

    df = pd.read_csv(INPUT_PATH)

    # =========================
    # FILTER LATAM + YEARS
    # =========================

    df = df[
        (df["country"].isin(LATAM_ISO3)) &
        (df["year"].between(START_YEAR, END_YEAR))
    ]

    if df.empty:
        raise ValueError("Dataset vacío después del filtrado")

    # =========================
    # RENAME
    # =========================

    df = df.rename(columns={
        "country": "country_code"
    })

    # =========================
    # SELECT
    # =========================

    cols = [
        "country_code",
        "year",
        "tourism_arrivals",
        "tourism_receipts",
        "tourism_departures"
    ]

    df = df[cols].dropna()

    # =========================
    # TYPES
    # =========================

    df["year"] = df["year"].astype(int)
    df["country_code"] = df["country_code"].astype(str)

    # =========================
    # PARTITION
    # =========================

    partitions = 0

    for (year, country), group in df.groupby(["year", "country_code"]):

        path = f"{OUTPUT_BASE}/year={year}/country_code={country}"
        file_path = f"{path}/data.parquet"

        partitions += 1

        if dry_run:
            logging.info(f"[DRY RUN] {file_path}")
        else:
            os.makedirs(path, exist_ok=True)

            group.to_parquet(
                file_path,
                index=False,
                compression="snappy"
            )

    logging.info(f"✅ Particiones: {partitions}")
    logging.info(f"🌎 Países: {df['country_code'].nunique()}")

# =========================
# CLI
# =========================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    process(dry_run=args.dry_run)