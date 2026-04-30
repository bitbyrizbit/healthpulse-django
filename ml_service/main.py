from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
from model import load_model

app = FastAPI(title="HealthPulse ML Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# load on startup
model, scaler = load_model()

LABELS = {0: "Low", 1: "Moderate", 2: "High"}


class HealthInput(BaseModel):
    age: int = Field(..., ge=1, le=120)
    weight_kg: float = Field(..., ge=20, le=300)
    height_cm: float = Field(..., ge=50, le=250)
    systolic_bp: int = Field(..., ge=80, le=250)
    diastolic_bp: int = Field(..., ge=40, le=150)
    blood_sugar: float = Field(..., ge=50, le=500)
    cholesterol: float = Field(..., ge=100, le=500)
    smoker: bool = False
    diabetic: bool = False


class PredictionOutput(BaseModel):
    risk_score: float
    risk_label: str
    bmi: float
    recommendations: list[str]


@app.get("/")
def root():
    return {"service": "HealthPulse ML API", "status": "running"}


@app.post("/predict", response_model=PredictionOutput)
def predict(data: HealthInput):
    h = data.height_cm / 100
    bmi = round(data.weight_kg / (h * h), 1)

    features = np.array([[
        data.age, bmi, data.systolic_bp, data.diastolic_bp,
        data.blood_sugar, data.cholesterol,
        int(data.smoker), int(data.diabetic)
    ]])

    features_scaled = scaler.transform(features)
    proba = model.predict_proba(features_scaled)[0]
    predicted_class = int(np.argmax(proba))
    risk_score = round(float(proba[predicted_class]), 3)
    risk_label = LABELS[predicted_class]

    # generate contextual recommendations
    recs = []
    if bmi > 25:
        recs.append("Consider weight management — BMI is above healthy range.")
    if data.systolic_bp > 130:
        recs.append("Monitor blood pressure regularly. Reduce sodium intake.")
    if data.blood_sugar > 140:
        recs.append("Elevated blood sugar detected. Consult an endocrinologist.")
    if data.cholesterol > 200:
        recs.append("High cholesterol — reduce saturated fats, increase exercise.")
    if data.smoker:
        recs.append("Smoking significantly increases cardiovascular risk. Quit smoking.")
    if not recs:
        recs.append("Your vitals look healthy. Keep up the good work!")

    return PredictionOutput(
        risk_score=risk_score,
        risk_label=risk_label,
        bmi=bmi,
        recommendations=recs
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}