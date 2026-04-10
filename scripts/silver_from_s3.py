import pandas as pd
import boto3
import os
import tempfile

# =========================
# CONFIG
# =========================

BUCKET = "tourism-co2-latam-sustentable"
PREFIX = "bronze/co2_emissions/"
OUTPUT_PATH = "data/silver/co2_latam_clean.parquet"

# =========================
# INIT
# =========================

s3 = boto3.client("s3")

# =========================
# LIST FILES (ROBUST)
# =========================

def list_parquet_files():
    print("🔍 Buscando archivos en S3...")

    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=BUCKET, Prefix=PREFIX)

    files = []

    for page in pages:
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".parquet"):
                files.append(obj["Key"])

    print(f"📦 Total archivos encontrados: {len(files)}")
    return files

# =========================
# READ FROM S3 (SAFE)
# =========================

def read_parquet_files(files):
    dfs = []

    for file in files:
        print(f"⬇️ Descargando: {file}")

        with tempfile.NamedTemporaryFile(suffix=".parquet") as tmp:
            s3.download_file(BUCKET, file, tmp.name)

            df = pd.read_parquet(tmp.name)
            dfs.append(df)

    print("📥 Todos los archivos descargados")
    return pd.concat(dfs, ignore_index=True)

# =========================
# TRANSFORM
# =========================

def transform(df):
    print("🧠 Transformando datos...")

    # eliminar nulos
    df = df.dropna()

    # tipos correctos
    df["year"] = df["year"].astype(int)

    # ordenar
    df = df.sort_values(["country_code", "year"])

    return df

# =========================
# SAVE
# =========================

def save(df):
    print("💾 Guardando capa silver...")

    os.makedirs("data/silver", exist_ok=True)

    df.to_parquet(
        OUTPUT_PATH,
        index=False,
        compression="snappy"
    )

    print(f"✅ Silver guardado en: {OUTPUT_PATH}")

# =========================
# MAIN
# =========================

def main():
    print("🚀 Iniciando pipeline SILVER desde S3\n")

    files = list_parquet_files()

    if not files:
        print("❌ No se encontraron archivos en S3")
        return

    df = read_parquet_files(files)

    df = transform(df)

    save(df)

    print("\n🎉 Pipeline SILVER completado")

# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()