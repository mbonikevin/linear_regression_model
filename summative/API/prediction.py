from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import numpy as np
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

app = FastAPI(title="student score predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:34065",
        "https://linear-regression-model-ihll.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# declaring my model and scaler files
folder = os.path.dirname(os.path.abspath(__file__))
my_model = joblib.load(os.path.join(folder, "../linear_regression/models/best_model.pkl"))
my_scaler = joblib.load(os.path.join(folder, "../linear_regression/models/scaler.pkl"))


class StudentInfo(BaseModel):
    hours_studied: int = Field(..., ge=1, le=44)
    attendance: float = Field(..., ge=0, le=100)
    parental_involvement: Literal["Low", "Medium", "High"]
    access_to_resources: Literal["Low", "Medium", "High"]
    extracurricular_activities: Literal["Yes", "No"]
    previous_scores: int = Field(..., ge=0, le=100)
    internet_access: Literal["Yes", "No"]
    tutoring_sessions: int = Field(..., ge=0, le=8)
    family_income: Literal["Low", "Medium", "High"]
    teacher_quality: Literal["Low", "Medium", "High"]
    peer_influence: Literal["Negative", "Neutral", "Positive"]
    physical_activity: int = Field(..., ge=0, le=6)
    learning_disabilities: Literal["Yes", "No"]
    parental_education_level: Literal["High School", "College", "Postgraduate"]
    distance_from_home: Literal["Near", "Moderate", "Far"]


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

    return {"predicted_exam_score": round(float(score), 2)}


@app.post("/retrain")
def retrain(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    if "Exam_Score" not in df.columns:
        raise HTTPException(status_code=400, detail="csv must have an Exam_Score column")

    to_drop = ["Sleep_Hours", "Motivation_Level", "School_Type", "Gender"]
    df.drop(columns=[c for c in to_drop if c in df.columns], inplace=True)

    ordinal_maps = {
        "Parental_Involvement": {"Low": 0, "Medium": 1, "High": 2},
        "Access_to_Resources": {"Low": 0, "Medium": 1, "High": 2},
        "Family_Income": {"Low": 0, "Medium": 1, "High": 2},
        "Teacher_Quality": {"Low": 0, "Medium": 1, "High": 2},
        "Parental_Education_Level": {"High School": 0, "College": 1, "Postgraduate": 2},
        "Distance_from_Home": {"Near": 0, "Moderate": 1, "Far": 2},
        "Peer_Influence": {"Negative": 0, "Neutral": 1, "Positive": 2},
    }
    binary_cols = ["Extracurricular_Activities", "Internet_Access", "Learning_Disabilities"]

    for col, mapping in ordinal_maps.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    le = LabelEncoder()
    for col in binary_cols:
        if col in df.columns:
            df[col] = le.fit_transform(df[col].astype(str))

    df.fillna(df.median(numeric_only=True), inplace=True)

    feature_cols = [
        "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
        "Extracurricular_Activities", "Previous_Scores", "Internet_Access", "Tutoring_Sessions",
        "Family_Income", "Teacher_Quality", "Peer_Influence", "Physical_Activity",
        "Learning_Disabilities", "Parental_Education_Level", "Distance_from_Home"
    ]

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"missing columns: {missing}")

    X = df[feature_cols]
    y = df["Exam_Score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    new_scaler = StandardScaler()
    X_train_scaled = new_scaler.fit_transform(X_train)

    new_model = LinearRegression()
    new_model.fit(X_train_scaled, y_train)

    global my_model, my_scaler
    my_model = new_model
    my_scaler = new_scaler

    models_dir = os.path.join(folder, "../linear_regression/models/")
    joblib.dump(new_model, models_dir + "best_model.pkl")
    joblib.dump(new_scaler, models_dir + "scaler.pkl")

    return {"message": "model retrained", "rows_used_for_training": len(X_train)}
