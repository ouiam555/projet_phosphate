import os
from pathlib import Path

from dotenv import load_dotenv
from minio import Minio

print("===== START =====")

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

print("Endpoint:", os.getenv("MINIO_ENDPOINT"))
print("Bucket:", os.getenv("MINIO_BUCKET"))
print("BASE_DIR:", BASE_DIR)

client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)

bucket = os.getenv("MINIO_BUCKET")

files = [
    BASE_DIR / "data/raw/prices.csv",
    BASE_DIR / "data/raw/production.csv",
    BASE_DIR / "data/raw/inflation_2016_2026.csv",
    BASE_DIR / "data/raw/import_2016_2026.csv",
    BASE_DIR / "data/raw/export_2016_2026.csv",
]

print(files)

if not client.bucket_exists(bucket):
    client.make_bucket(bucket)

for file in files:

    print(file)

    if not file.exists():
        print("NOT FOUND")
        continue

    print("Uploading", file.name)

    client.fput_object(
        bucket_name=bucket,
        object_name=file.name,
        file_path=str(file),
    )

    print(file.name, "uploaded")

print("DONE")