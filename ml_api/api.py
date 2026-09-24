from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path


app = FastAPI(
    title="Vehicle Resale Price Prediction API",
    description="API for predicting vehicle resale prices",
    version="1.0.0"
)


# Load trained ML model
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "vehicle_price_model.pkl"

model = joblib.load(MODEL_PATH)


class VehicleInput(BaseModel):
    brand: str
    model: str
    year: int
    mileage: int
    engine_capacity: int
    fuel_type: str
    transmission: str
    condition: str
    location: str


@app.get("/")
def root():
    return {
        "message": "Vehicle Resale Price Prediction API is running"
    }


@app.post("/predict")
def predict_price(vehicle: VehicleInput):

    input_data = pd.DataFrame([{
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "mileage": vehicle.mileage,
        "engine_capacity": vehicle.engine_capacity,
        "fuel_type": vehicle.fuel_type,
        "transmission": vehicle.transmission,
        "condition": vehicle.condition,
        "location": vehicle.location,
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_price": round(float(prediction), 2)
    }