# HealthPulse 🩺

A full-stack health assistant web application built as part of the Web Development Lab (WDL) mini project. Users can register, book doctor appointments, and run an AI-powered health risk assessment based on their vitals.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 + Django REST Framework |
| ML Microservice | FastAPI + scikit-learn |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript (vanilla) |

## Features

- User registration, login, logout with session-based auth
- Book, view, and cancel doctor appointments
- Health risk checker form (age, weight, BP, blood sugar, cholesterol)
- ML model (Random Forest) predicts cardiovascular risk — Low / Moderate / High
- REST API endpoints for appointments, doctors, and health records
- JS form validation on all input forms
- Admin panel for managing doctors and appointments

## Experiments Covered (3–13)

| Exp | Description | Implementation |
|-----|-------------|---------------|
| 3 | JS Form Validation | Register, booking, and health checker forms |
| 4 | Django views rendering templates | All app views with static + dynamic content |
| 5 | RESTful API serving JSON | DRF endpoints for doctors and appointments |
| 6 | FastAPI with auto data validation | `ml_service/main.py` with Pydantic schemas |
| 7 | ML model as API endpoint | Random Forest risk predictor via FastAPI |
| 8 | Django project + models + views | Full Django project with 3 apps |
| 9 | CRUD operations | Create, Read, Update (cancel) appointments |
| 10 | User authentication | Register, login, logout, session auth |
| 11 | Django REST Framework API | ViewSets + Routers for all resources |
| 12 | PostgreSQL + migrations | Full DB setup with Django migrations |
| 13 | Frontend calling ML API | JS fetch → FastAPI prediction endpoint |

## Project Structure

```
healthpulse-django/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── healthpulse/        # Django config
│   ├── accounts/           # Auth app
│   ├── appointments/       # Booking app
│   └── health/             # Health checker app
├── ml_service/
│   ├── main.py             # FastAPI app
│   ├── model.py            # ML model training + inference
│   └── requirements.txt
└── README.md
```

## Local Setup

### Prerequisites
- Python 3.10+
- PostgreSQL

### 1. Clone the repo
```bash
git clone https://github.com/bitbyrizbit/healthpulse-django.git
cd healthpulse-django
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file inside `backend/`:
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=healthpulse_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 5. Setup database
```bash
# In psql
CREATE DATABASE healthpulse_db;
```

### 6. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Start Django server
```bash
python manage.py runserver
```

### 8. Start FastAPI ML service (separate terminal)
```bash
cd ml_service
pip install -r requirements.txt
uvicorn main:app --port 8001 --reload
```

Visit: `http://127.0.0.1:8000/accounts/register/`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/appointments/doctors/` | List all doctors |
| GET/POST | `/api/appointments/appointments/` | List / create appointments |
| PATCH | `/api/appointments/appointments/{id}/cancel/` | Cancel appointment |
| GET/POST | `/api/health/records/` | List / create health records |
| POST | `http://localhost:8001/predict` | ML risk prediction |

