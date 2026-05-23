import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
import joblib

print("Generating smart grid telemetry data...")
# Simulating 4 features: [Solar Output (kW), Battery Charge %, Current Grid Price (cents), Household Demand (kW)]
X_raw, y_raw = make_classification(n_samples=1000, n_features=4, n_informative=4, n_redundant=0, random_state=42)

df = pd.DataFrame(X_raw, columns=['solar_output', 'battery_level', 'grid_price', 'house_demand'])

# Train AI baseline model
model = RandomForestClassifier(random_state=42)
model.fit(df, y_raw)

# Save the finished model into a file asset called 'energy_router.joblib'
joblib.dump(model, "energy_router.joblib")
print("🎉 Success! 'energy_router.joblib' model file has been created.")