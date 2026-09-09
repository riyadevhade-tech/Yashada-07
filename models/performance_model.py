import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load analyzed dataset
df = pd.read_csv("data/analyzed_sports_performance.csv")

# Features used for prediction
features = [
    "Points",
    "Assists",
    "Accuracy",
    "Speed",
    "Stamina",
    "Training_Hours",
    "Wins"
]

X = df[features]
y = df["Performance_Score"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create AI model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("\n========================================")
print("       AI SPORT PERFORMANCE MODEL")
print("========================================")

print("\nModel Training: Completed")
print("Model Testing: Completed")
print("Mean Absolute Error:", round(mae, 2))

# Save trained model
with open("models/performance_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nAI model saved successfully!")
print("File: models/performance_model.pkl")