import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'health_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')


def train_and_save():
    """
    Trains a simple health risk classifier on synthetic data.
    In a real project, replace with actual dataset.
    """
    np.random.seed(42)
    n = 1000

    # synthetic features: age, bmi, systolic_bp, diastolic_bp, blood_sugar, cholesterol, smoker, diabetic
    age = np.random.randint(18, 80, n)
    bmi = np.random.uniform(16, 42, n)
    sys_bp = np.random.randint(90, 180, n)
    dia_bp = np.random.randint(60, 110, n)
    sugar = np.random.uniform(70, 250, n)
    chol = np.random.uniform(120, 320, n)
    smoker = np.random.randint(0, 2, n)
    diabetic = np.random.randint(0, 2, n)

    X = np.column_stack([age, bmi, sys_bp, dia_bp, sugar, chol, smoker, diabetic])

    # simple rule-based labeling for synthetic ground truth
    risk = (
        (sys_bp > 140).astype(int) +
        (sugar > 180).astype(int) +
        (chol > 240).astype(int) +
        (bmi > 30).astype(int) +
        smoker + diabetic
    )
    y = np.where(risk >= 4, 2, np.where(risk >= 2, 1, 0))  # 0=Low, 1=Moderate, 2=High

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print("Model trained and saved.")


def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save()
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler