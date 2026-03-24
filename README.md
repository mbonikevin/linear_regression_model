# Predicting Student Exam Scores Using Regression Models

## Mission
This project is trying to predict how well a student will score on their exam based on things like how many hours they study, their attendance, whether their parents are involved and other factors. the idea is that if we can predict low scores early, teachers can step in and help those students before it is too late

The dataset that was used is the **Student Performance Factors** dataset from Kaggle, it has about 6607 rows and 20 columns covering a mix of numeric and categorical features like study hours, sleep, motivation level, internet access, and parental education, the target column we are trying to predict is ```Exam Score```
Dataset source: https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
Models being used: linear regression, decision tree regressor, and random forest regressor, all from scikit-learn


## Repo structure

```
linear_regression_model/
|
|-- summative/
|   |-- API/
|   |   |-- prediction.py
|   |   |-- requirements.txt
|   |-- FlutterApp/
|   |-- linear_regression/
|   |   |-- models/
|   |   |   |-- best_model.pkl
|   |   |   |-- scaler.pkl
|   |   |-- multivariate.ipynb
|   |   |-- StudentPerformanceFactors.csv
```

## Models used (from scikit-learn)
- linear regression (best performing)
- decision tree regressor
- random forest regressor

the best performing model gets saved to be used in the API

## How to run the notebook
1. Create a virtual environment and install dependencies:
   - create the venv: python3 -m venv venv
   - activate it (linux/mac): source venv/bin/activate
   - activate it (windows): venv\Scripts\activate
   - install packages: pip install ipykernel numpy pandas matplotlib seaborn scikit-learn joblib
2. Open the notebook in vscode, press `ctrl+shift+p`, type "**Python: Select Interpreter**" and select the **venv option (./venv/bin/python)**
   - if the kernel still fails, click `Change Kernel` in the popup and select the **venv interpreter** from the list
   - if you still don't see it, click `Enter interpreter path` and type **./venv/bin/python** manually
3. Run all cells from top to bottom

## How to run the API locally
1. Activate the virtual environment and install the api dependencies:
   - source venv/bin/activate
   - pip install -r summative/API/requirements.txt
2. Start the server:
   - uvicorn summative.API.prediction:app --reload
3. Open your browser and go to http://127.0.0.1:8000/docs and test the API

## How to run the Flutter app
1. Make sure you have Flutter installed: https://docs.flutter.dev/get-started/install
2. Connect an Android or iOS device, or start an emulator
3. Navigate to the Flutter app folder:
   - cd summative/FlutterApp
4. Install dependencies:
   - flutter pub get
5. Run the app:
   - flutter run

## Video Demo
[link to video demo on YouTube](https://youtu.be/VDZeyNBkD-k)

## Live API
The API is hosted on Render: [https://linear-regression-model-ihll.onrender.com/docs](https://linear-regression-model-ihll.onrender.com/docs)

use the `/docs` page to test it interactively and the `/predict` endpoint to make predictions and also the `/retrain` endpoint to retrain the model by uploading a new csv file
