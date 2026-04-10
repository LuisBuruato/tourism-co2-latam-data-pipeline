import pandas as pd

# =========================
# CONFIG
# =========================

INPUT_PATH = "data/raw/owid-co2-data.csv"

LATAM_COUNTRIES = [
    "Argentina","Bolivia","Brazil","Chile","Colombia","Costa Rica",
    "Cuba","Dominican Republic","Ecuador","El Salvador","Guatemala",
    "Honduras","Mexico","Nicaragua","Panama","Paraguay","Peru",
    "Uruguay","Venezuela"
]

# mapping a códigos ISO (para unir con World Bank)
COUNTRY_MAPPING = {
    "Argentina": "ARG",
    "Bolivia": "BOL",
    "Brazil": "BRA",
    "Chile": "CHL",
    "Colombia": "COL",
    "Costa Rica": "CRI",
    "Cuba": "CUB",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "El Salvador": "SLV",
    "Guatemala": "GTM",
    "Honduras": "HND",
    "Mexico": "MEX",
    "Nicaragua": "NIC",
    "Panama": "PAN",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Uruguay": "URY",
    "Venezuela": "VEN"
}

# =========================
# FUNCTION
# =========================

def get_co2_data():
    print("🌫️ Cargando CO₂ desde OWID...")

    df = pd.read_csv(INPUT_PATH)

    # filtrar LATAM
    df = df[df["country"].isin(LATAM_COUNTRIES)]

    # seleccionar columnas
    df = df[["country", "year", "co2"]]

    # mapear a códigos
    df["country"] = df["country"].map(COUNTRY_MAPPING)

    # limpiar
    df = df.dropna(subset=["country", "year", "co2"])

    df["year"] = df["year"].astype(int)

    print("✅ CO₂ listo")
    print(df.head())

    return df


# =========================
# TEST
# =========================

if __name__ == "__main__":
    get_co2_data()