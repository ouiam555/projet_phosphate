import os
from pathlib import Path

from dotenv import load_dotenv
from minio import Minio

load_dotenv()

client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

BUCKET = os.getenv("MINIO_BUCKET")

BASE_DIR = Path(__file__).resolve().parents[2]

TEMP_DIR = BASE_DIR / "data" / "temp"

TEMP_DIR.mkdir(parents=True, exist_ok=True)


def download_file(object_name):

    destination = TEMP_DIR / object_name

    client.fget_object(
        bucket_name=BUCKET,
        object_name=object_name,
        file_path=str(destination)
    )

    print(f"Downloaded : {object_name}")

    return destination