from load_data import load_data
from feature_engineering import create_features

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


# -----------------------
# Load Data
# -----------------------

df = load_data()
df = create_features(df)


# -----------------------
# Features & Target
# -----------------------

X = df.drop(
    columns=[
        "DATE",
        "PHOSPHATE_PRICE_USD"
    ]
)

y = df["PHOSPHATE_PRICE_USD"]


# -----------------------
# Train/Test Split
# -----------------------

train = df.iloc[:-12]
test = df.iloc[-12:]

X_train = train.drop(columns=["DATE", "PHOSPHATE_PRICE_USD"])
y_train = train["PHOSPHATE_PRICE_USD"]

X_test = test.drop(columns=["DATE", "PHOSPHATE_PRICE_USD"])
y_test = test["PHOSPHATE_PRICE_USD"]


# -----------------------
# Train Model
# -----------------------

model = LinearRegression()

model.fit(X_train, y_train)


# -----------------------
# Prediction
# -----------------------

predictions = model.predict(X_test)


# -----------------------
# Evaluation
# -----------------------

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(mean_squared_error(y_test, predictions))

r2 = r2_score(y_test, predictions)


print("\n===== Linear Regression =====")

print(f"Training rows : {len(train)}")
print(f"Testing rows  : {len(test)}")

print(f"\nMAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

print("\nPredictions")

results = test[["DATE", "PHOSPHATE_PRICE_USD"]].copy()
results["Predicted"] = predictions

print(results)