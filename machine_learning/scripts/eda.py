import matplotlib.pyplot as plt

from load_data import load_data


df = load_data()

plt.figure(figsize=(12, 5))
plt.plot(
    df["PHOSPHATE_PRICE_USD"],
    marker="o"
)

plt.title("Phosphate Price Over Time")
plt.xlabel("Month")
plt.ylabel("Price (USD)")
plt.grid(True)

plt.show()