import pandas as pd
import boto3
import os

# =========================
# CONFIG
# =========================

BUCKET = "tourism-co2-latam-sustentable"
PREFIX = "bronze/co2_emissions/"
OUTPUT_PATH = "data/silver/co2_latam_clean.parquet"

# =========================
# S3 CLIENT
# =========================

s3 = boto3.client("s3")

# =========================
# LIST FILES
# =========================

def list_parquet_files():
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)

    files = []
    for obj in response.get("Contents", []):
        if obj["Key"].endswith(".parquet"):
            files.append(obj["Key"])

    return files

# =========================
# READ PARQUET FROM S3
# =========================

def read_parquet_files(files):
    dfs = []

    for file in files:
        s3_path = f"s3://{BUCKET}/{file}"
        df = pd.read_parquet(s3_path)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

# =========================
# TRANSFORM
# =========================

def transform(df):
    # limpiar nulos
    df = df.dropna()

    # ordenar
    df = df.sort_values(["country_code", "year"])

    return df

# =========================
# SAVE SILVER
# =========================

def save(df):
    os.makedirs("data/silver", exist_ok=True)

    df.to_parquet(OUTPUT_PATH, index=False)

    print(f"✅ Silver guardado en: {OUTPUT_PATH}")

# =========================
# MAIN
# =========================

def main():
    print("☁️ Leyendo bronze desde S3...")

    files = list_parquet_files()
    print(f"📦 Archivos encontrados: {len(files)}")

    df = read_parquet_files(files)

    print("🧠 Transformando...")
    df = transform(df)

    print("💾 Guardando silver...")
    save(df)

    print("🎉 Pipeline silver completo")

if __name__ == "__main__":
    main()