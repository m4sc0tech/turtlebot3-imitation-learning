import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import joblib

# --- Step A: Load the CSV ---
df = pd.read_csv('/home/matias/turtlebot3_ws/turtlebot3_data.csv')
print("Raw shape:", df.shape)

# --- Step A.5: Clean invalid LiDAR values (inf = no return / out of range) ---
range_cols = [c for c in df.columns if c.startswith('range_')]
df[range_cols] = df[range_cols].replace([np.inf, -np.inf], 10.0)
df[range_cols] = df[range_cols].fillna(10.0)

# --- Step B: Remove idle rows (robot not moving) ---
df = df[~((df['linear_x'] == 0.0) & (df['angular_z'] == 0.0))]
print("Shape after removing idle rows:", df.shape)

# --- Step C: Split into X (inputs) and y (outputs) ---
X = df.iloc[:, 2:-2]
y = df.iloc[:, -2:]
print("X shape:", X.shape)
print("y shape:", y.shape)

# --- Step D: Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Step E: Train the model ---
model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
model.fit(X_train, y_train)

# --- Step F: Evaluate ---
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("Test MSE:", mse)
print("Train score (R^2):", model.score(X_train, y_train))
print("Test score (R^2):", model.score(X_test, y_test))

# --- Step G: Save the trained model ---
joblib.dump(model, '/home/matias/turtlebot3_ws/model.pkl')
print("Model saved to model.pkl")
