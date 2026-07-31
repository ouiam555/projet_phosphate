from load_data import load_data
from feature_engineering import create_features

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


# Load and prepare data
df = load_data()
df = create_features(df)


# Time-based split
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


# Create model
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)


# Train model
model.fit(X_train, y_train)


# Predictions
predictions = model.predict(X_test)


# Metrics
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)


print("\n===== Random Forest =====")

print(f"Training rows : {len(train)}")
print(f"Testing rows  : {len(test)}")

print(f"\nMAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")


# Results
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

print("\nPredictions")
print(results)


# Feature importance
importance = (
    model.feature_importances_
)

feature_importance = (
    X_train.columns
    .to_frame(index=False, name="Feature")
)

feature_importance["Importance"] = importance

feature_importance = (
    feature_importance
    .sort_values(
        by="Importance",
        ascending=False
    )
)

print("\n===== Feature Importance =====")
print(feature_importance.head(10))