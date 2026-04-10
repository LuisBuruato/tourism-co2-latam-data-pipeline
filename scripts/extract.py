import requests
import pandas as pd
import time
import os

# =========================
# CONFIG
# =========================

COUNTRIES = [
    "ARG","BOL","BRA","CHL","COL","CRI","CUB","DOM","ECU",
    "SLV","GTM","HND","MEX","NIC","PAN","PRY","PER","URY","VEN"
]


INDICATORS = {
    "tourism_arrivals": "ST.INT.ARVL",
    "tourism_receipts": "ST.INT.RCPT.CD",
    "tourism_departures": "ST.INT.DPRT",
    "gdp": "NY.GDP.MKTP.CD",
    "renewable_energy": "EG.FEC.RNEW.ZS",

}

BASE_URL = "http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1000"

OUTPUT_PATH = "data/raw/tourism_co2_latam_raw.csv"


# =========================
# CREATE FOLDERS
# =========================

def ensure_folders():
    os.makedirs("data/raw", exist_ok=True)


# =========================
# FETCH WITH RETRY
# =========================

def fetch_indicator(country, indicator_name, indicator_code):
    url = BASE_URL.format(country=country, indicator=indicator_code)

    for attempt in range(3):  # 🔁 reintentos
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            if len(data) < 2:
                print(f"⚠️ No data for {country} - {indicator_name}")
                return pd.DataFrame()

            rows = []
            for item in data[1]:
                rows.append({
                    "country": country,
                    "year": item["date"],
                    indicator_name: item["value"]
                })

            return pd.DataFrame(rows)

        except Exception as e:
            print(f"⚠️ Retry {attempt+1}/3 → {country} - {indicator_name}")
            time.sleep(2)

    print(f"❌ Failed after retries: {country} - {indicator_name}")
    return pd.DataFrame()


# =========================
# MAIN EXTRACT
# =========================

def extract_all():
    print("🔥 Script corriendo...\n")
    print("🚀 Iniciando extracción...\n")

    ensure_folders()

    dfs = []

    for indicator_name, indicator_code in INDICATORS.items():
        print(f"📊 Extrayendo: {indicator_name}")

        temp_dfs = []

        for country in COUNTRIES:
            df = fetch_indicator(country, indicator_name, indicator_code)

            if not df.empty:
                temp_dfs.append(df)

            time.sleep(0.5)  # 🐢 evitar rate limit

        if temp_dfs:
            df_indicator = pd.concat(temp_dfs, ignore_index=True)
            dfs.append(df_indicator)

    # =========================
    # MERGE FINAL
    # =========================

    print("\n🔗 Uniendo datasets...")

    if not dfs:
        print("❌ No se pudo extraer ningún dataset")
        return

    df_final = dfs[0]

    for df in dfs[1:]:
        df_final = df_final.merge(df, on=["country", "year"], how="outer")

    # =========================
    # CLEAN BASIC
    # =========================

    df_final["year"] = pd.to_numeric(df_final["year"], errors="coerce")
    df_final = df_final.dropna(subset=["year"])
    df_final["year"] = df_final["year"].astype(int)

    df_final = df_final.sort_values(["country", "year"])

    # =========================
    # SAVE
    # =========================

    df_final.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Archivo guardado en: {OUTPUT_PATH}")
    print("\n📊 Preview:")
    print(df_final.head())


# =========================
# RUN
# =========================

if __name__ == "__main__":
    extract_all()