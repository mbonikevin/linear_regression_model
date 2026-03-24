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


@app.get("/")
def home():
    return "Hi, my student exam score predictor is running, you can go to /docs and try it out"


@app.post("/predict")
def predict(info: StudentInfo):
    # mapping the text inputs to numbers the same way i did in the notebook
    level_map = {"Low": 0, "Medium": 1, "High": 2}
    yes_no = {"Yes": 1, "No": 0}
    edu_map = {"High School": 0, "College": 1, "Postgraduate": 2}
    dist_map = {"Near": 0, "Moderate": 1, "Far": 2}
    peer_map = {"Negative": 0, "Neutral": 1, "Positive": 2}

    # putting all the values in the same order as the training data
    values = [
        info.hours_studied,
        info.attendance,
        level_map.get(info.parental_involvement, 1),
        level_map.get(info.access_to_resources, 1),
        yes_no.get(info.extracurricular_activities, 0),
        info.previous_scores,
        yes_no.get(info.internet_access, 1),
        info.tutoring_sessions,
        level_map.get(info.family_income, 1),
        level_map.get(info.teacher_quality, 1),
        peer_map.get(info.peer_influence, 1),
        info.physical_activity,
        yes_no.get(info.learning_disabilities, 0),
        edu_map.get(info.parental_education_level, 1),
        dist_map.get(info.distance_from_home, 0),
    ]

    # scale and predict
    nums = np.array(values).reshape(1, -1)
    scaled = my_scaler.transform(nums)
    score = my_model.predict(scaled)[0]

    return {"predicted exam score is: ": round(float(score), 2)}
