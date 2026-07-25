import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = "https://www.indexmundi.com/commodities/?commodity=rock-phosphate&months=300"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

text = soup.get_text("\n")

# Exemple de ligne :
# Jan 2016 122.60 -0.73%

pattern = r'([A-Z][a-z]{2})\s(20(?:1[6-9]|2[0-6]))\s([0-9]+(?:\.[0-9]+)?)'

matches = re.findall(pattern, text)

rows = []

for month, year, price in matches:

    rows.append({
        "year": int(year),
        "month": month,
        "price_usd_per_metric_ton": float(price)
    })

df = pd.DataFrame(rows)

# garder seulement 2016 -> 2026
df = df[(df["year"] >= 2016) & (df["year"] <= 2026)]

# supprimer doublons éventuels
df = df.drop_duplicates()

# ordre chronologique
months = {
    "Jan":1,"Feb":2,"Mar":3,"Apr":4,
    "May":5,"Jun":6,"Jul":7,"Aug":8,
    "Sep":9,"Oct":10,"Nov":11,"Dec":12
}

df["month_number"] = df["month"].map(months)

df = df.sort_values(["year","month_number"])

df.drop(columns="month_number", inplace=True)

print(df)

print("\nNombre de lignes :", len(df))

df.to_csv("phosphate_price_monthly_2016_2026.csv", index=False)

print("\nCSV créé : phosphate_price_monthly_2016_2026.csv")