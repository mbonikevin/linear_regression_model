from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os

app = FastAPI(title="student score predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# declaring my model and scaler files
folder = os.path.dirname(os.path.abspath(__file__))
my_model = joblib.load(os.path.join(folder, "../linear_regression/models/best_model.pkl"))
my_scaler = joblib.load(os.path.join(folder, "../linear_regression/models/scaler.pkl"))


class StudentInfo(BaseModel):
    hours_studied: int = Field(..., ge=1, le=44)
    attendance: float = Field(..., ge=0, le=100)
    parental_involvement: str  # valid values: Low, Medium, High
    access_to_resources: str  # valid values: Low, Medium, High
    extracurricular_activities: str  # valid values: Yes, No
    previous_scores: int = Field(..., ge=0, le=100)
    internet_access: str  # valid values: Yes, No
    tutoring_sessions: int = Field(..., ge=0, le=8)
    family_income: str  # valid values: Low, Medium, High
    teacher_quality: str  # valid values: Low, Medium, High
    peer_influence: str  # valid values: Negative, Neutral, Positive
    physical_activity: int = Field(..., ge=0, le=6)
    learning_disabilities: str  # valid values: Yes, No
    parental_education_level: str  #valid values: High School, College, Postgraduate
    distance_from_home: str  # valid values: Near, Moderate, Far
