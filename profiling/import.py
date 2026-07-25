import pandas as pd

# ==============================
# Configuration
# ==============================

FILE_PATH = r"C:\Users\HP\Desktop\projet2\data\raw\import_2016_2026.csv"

# ==============================
# Load Data
# ==============================

df = pd.read_csv(FILE_PATH)

# ==============================
# General Information
# ==============================

print("=" * 60)
print("DATA PROFILING REPORT")
print("=" * 60)

print(f"\nRows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nColumn Names")
print(df.columns.tolist())

print("\nData Types")
print(df.dtypes)

# ==============================
# Missing Values
# ==============================

print("\nMissing Values")
print(df.isnull().sum())

# ==============================
# Duplicate Rows
# ==============================

duplicates = df.duplicated().sum()

print("\nDuplicate Rows")
print(duplicates)

# ==============================
# Memory Usage
# ==============================

memory = df.memory_usage(deep=True).sum() / 1024**2

print(f"\nMemory Usage : {memory:.2f} MB")

# ==============================
# Statistics
# ==============================

print("\nStatistics")
print(df.describe(include="all"))

# ==============================
# First Rows
# ==============================

print("\nFirst 5 Rows")
print(df.head())

# ==============================
# Last Rows
# ==============================

print("\nLast 5 Rows")
print(df.tail())