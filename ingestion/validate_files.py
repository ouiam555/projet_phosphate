from pathlib import Path

import pandas as pd


RAW_DIR = Path("/opt/project/data/raw")

EXPECTED_FILES = {
    "prices.csv": None,
    "production.csv": None,
    "inflation_2016_2026.csv": None,
    "import_2016_2026.csv": None,
    "export_2016_2026.csv": None,
}


def validate_csv(
    file_path: Path,
    expected_columns: list[str] | None = None,
) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    if file_path.stat().st_size == 0:
        raise ValueError(f"Empty file: {file_path.name}")

    try:
        dataframe = pd.read_csv(file_path, low_memory=False)
    except Exception as exc:
        raise ValueError(
            f"Cannot read file {file_path.name}: {exc}"
        ) from exc

    if dataframe.empty:
        raise ValueError(f"No data rows found in: {file_path.name}")

    if expected_columns:
        missing_columns = [
            column
            for column in expected_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{file_path.name} missing columns: {missing_columns}"
            )

    row_count = len(dataframe)
    column_count = len(dataframe.columns)
    duplicate_count = int(dataframe.duplicated().sum())
    null_count = int(dataframe.isna().sum().sum())

    print("=" * 60)
    print(f"File: {file_path.name}")
    print(f"Rows: {row_count}")
    print(f"Columns: {column_count}")
    print(f"Duplicates: {duplicate_count}")
    print(f"Null values: {null_count}")
    print(f"Size: {file_path.stat().st_size} bytes")

    if column_count == 0:
        raise ValueError(f"No columns found in: {file_path.name}")


def main() -> None:
    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"RAW directory not found: {RAW_DIR}"
        )

    print("Starting raw CSV validation...")

    for filename, expected_columns in EXPECTED_FILES.items():
        validate_csv(
            file_path=RAW_DIR / filename,
            expected_columns=expected_columns,
        )

    print("=" * 60)
    print("All raw CSV files passed validation successfully.")


if __name__ == "__main__":
    main()