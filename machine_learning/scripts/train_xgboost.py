from load_data import load_data
from feature_engineering import create_features

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


# --------------------------
# Load Data
# --------------------------

df = load_data()
df = create_features(df)


# --------------------------
# Train/Test Split
# --------------------------

train = df.iloc[:-12]
test = df.iloc[-12:]


X_train = train.drop(
    columns=[
        "DATE",
        "PHOSPHATE_PRICE_USD"
    ]
)

y_train = train["PHOSPHATE_PRICE_USD"]


X_test = test.drop(
    columns=[
        "DATE",
        "PHOSPHATE_PRICE_USD"
    ]
)

y_test = test["PHOSPHATE_PRICE_USD"]


# --------------------------
# XGBoost Model
# --------------------------

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)


# --------------------------
# Training
# --------------------------

model.fit(X_train, y_train)


# --------------------------
# Prediction
# --------------------------

predictions = model.predict(X_test)


# --------------------------
# Metrics
# --------------------------

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

r2 = r2_score(
    y_test,
    predictions
)


print("\n===== XGBoost =====")

print(f"Training rows : {len(train)}")
print(f"Testing rows  : {len(test)}")

print(f"\nMAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")


# --------------------------
# Predictions
# --------------------------

results = test[
    [
        "DATE",
        "PHOSPHATE_PRICE_USD"
    ]
].copy()

results["Predicted"] = predictions

results["Absolute_Error"] = abs(
    results["PHOSPHATE_PRICE_USD"] -
    results["Predicted"]
)

print("\n===== Predictions =====")
print(results)


# --------------------------
# Feature Importance
# --------------------------

importance = model.feature_importances_

features = X_train.columns

ranking = (
    list(zip(features, importance))
)

ranking = sorted(
    ranking,
    key=lambda x: x[1],
    reverse=True
)

print("\n===== Feature Importance =====")

for feature, score in ranking:
    print(f"{feature:<30} {score:.4f}")