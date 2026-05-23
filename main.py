from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Smart Grid Energy Router API")

# Load trained model file straight into memory
model = joblib.load("energy_router.joblib")

# Tell API exactly what inputs to expect from a smart meter
class SmartMeterReading(BaseModel):
    solar_output: float
    battery_level: float
    grid_price: float
    house_demand: float

@app.get("/")
def home():
    return {"status": "Energy Router Online and Live!"}

@app.post("/route-power")
def route_power(reading: SmartMeterReading):
    features = np.array([[reading.solar_output, reading.battery_level, reading.grid_price, reading.house_demand]])
    
    # Run the model calculation
    prediction = int(model.predict(features)[0])
    
    # Translate the machine learning output into clean, human business logic
    if reading.solar_output > 3.5 and reading.battery_level > 80:
        action = "SURPLUS_MODE"
        directive = "Solar output is high and battery is full. Directing excess clean energy to charge the Electric Vehicle and selling the remainder back to the city grid."
    elif reading.grid_price > 25.0:
        action = "PEAK_SAVING_MODE"
        directive = "Grid electricity prices are critically high. Disconnecting house from city grid; running appliances entirely off internal home battery storage."
    else:
        action = "STANDARD_BALANCED_MODE"
        directive = "Normal operating conditions. Blending solar generation with minimal grid baseline power."

    return {
        "automation_status": action,
        "system_directive": directive,
        "grid_stress_index": "HIGH" if prediction == 1 else "STABLE"
    }