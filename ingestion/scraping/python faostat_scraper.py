import requests
import pandas as pd

# World Bank Indicator:
# FP.CPI.TOTL.ZG = Inflation, consumer prices (annual %)

URL = (
    "https://api.worldbank.org/v2/"
    "country/all/"
    "indicator/FP.CPI.TOTL.ZG"
    "?format=json"
    "&per_page=30000"
)

response = requests.get(URL)
response.raise_for_status()

data = response.json()

records = []

for row in data[1]:
    if row["date"] is None:
        continue

    year = int(row["date"])

    if 2016 <= year <= 2026:
        records.append({
            "country": row["country"]["value"],
            "country_code": row["countryiso3code"],
            "year": year,
            "inflation": row["value"]
        })

df = pd.DataFrame(records)

# حذف الصفوف اللي ما فيهاش قيمة
df = df.dropna(subset=["inflation"])

# ترتيب
df = df.sort_values(["country", "year"])

# حفظ
df.to_csv("inflation_2016_2026.csv", index=False)

print(df.head())
print(f"\nNombre de lignes : {len(df)}")
print("Fichier créé : inflation_2016_2026.csv")