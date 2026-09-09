import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


# Load dataset
df = pd.read_csv("data/sports_performance.csv")


# Features used by AI model
features = [
    "Matches",
    "Points",
    "Assists",
    "Accuracy",
    "Speed",
    "Stamina",
    "Training_Hours",
    "Wins"
]


# Create target performance score
df["Performance_Score"] = (
    df["Points"] * 0.25
    + df["Accuracy"] * 0.20
    + df["Speed"] * 0.15
    + df["Stamina"] * 0.15
    + (df["Wins"] / df["Matches"] * 100) * 0.15
    + (df["Training_Hours"] / 20 * 100).clip(upper=100) * 0.10
)


X = df[features]
y = df["Performance_Score"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# AI Model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Prediction
predictions = model.predict(X_test)


# Evaluation
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)


print("\n======================================")
print("      AI PERFORMANCE PREDICTION")
print("======================================")

print("\nModel: Random Forest Regressor")

print("Mean Absolute Error:", round(mae, 2))
print("R2 Score:", round(r2, 2))

print("\nModel Training Completed Successfully!")

# Save model
joblib.dump(model, "models/performance_model.pkl")

print("\nModel saved successfully:")
print("models/performance_model.pkl")

print("======================================")