from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import sqlite3

app = FastAPI(title="Smart Grid Energy Router API")

# Load trained model file straight into memory
model = joblib.load("energy_router.joblib")

# Tell API exactly what inputs to expect from a smart meter
class SmartMeterReading(BaseModel):
    solar_output: float
    battery_level: float
    grid_price: float
    house_demand: float
# Create a local SQL database and a table for logs if it doesn't exist
conn = sqlite3.connect("smart_grid.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        solar REAL,
        battery REAL,
        price REAL,
        demand REAL,
        status TEXT
    )
""")
conn.commit()
conn.close()

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
# Run a SQL Query to insert the live data into our database
db_conn = sqlite3.connect("smart_grid.db")
db_cursor = db_conn.cursor()
db_cursor.execute(
    "INSERT INTO energy_logs (solar, battery, price, demand, status) VALUES (?, ?, ?, ?, ?)",
    (reading.solar_output, reading.battery_level, reading.grid_price, reading.house_demand, action)
)
db_conn.commit()
db_conn.close()

    return {
        "automation_status": action,
        "system_directive": directive,
        "grid_stress_index": "HIGH" if prediction == 1 else "STABLE"
    }
