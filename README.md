# Student Placement Prediction System

## Overview

This project is an end-to-end Machine Learning application that predicts whether a student is likely to be placed based on academic and skill-related attributes.

The system includes:

* Machine Learning model training using Logistic Regression
* Polynomial Feature Engineering
* Data Scaling and Preprocessing Pipeline
* Streamlit Web Application
* SQLite Database Integration
* Feedback Collection System
* Model Retraining Pipeline
* Interactive Dashboard

---

## Features

### Placement Prediction

Users can enter student information such as:

* IQ
* CGPA
* Academic Performance
* Internship Experience
* Extra-Curricular Score
* Communication Skills
* Projects Completed

The application predicts placement probability and placement status.

---

### Feedback Collection

Users can submit actual placement outcomes after receiving predictions.

This data is stored in the SQLite database and can later be used for retraining the model.

---

### Model Retraining

Verified feedback records can be merged with the original dataset and used to retrain the model, allowing continuous improvement.

---

### Dashboard

The dashboard provides:

* Total Predictions
* Predicted Placements
* Predicted Non-Placed Students
* Feedback Received
* Pending Feedback
* Live Prediction Accuracy

---

## Technologies Used

* Python
* Scikit-Learn
* Streamlit
* SQLite
* Pandas
* NumPy
* Joblib

---

## Project Structure

Student-Placement-Predictor/

├── app.py

├── predict.py

├── db.py

├── train.py

├── retrain.py

├── placement_predictor.pkl

├── placement.db

├── pages/

  ├── Feedback.py

  └── Dashboard.py

├── data/

  └── final_data.csv

├── requirements.txt

└── README.md

---

## Installation

Clone the repository:

git clone <repository-url>

Install dependencies:

pip install -r requirements.txt

Run the application:

python -m streamlit run app.py

---

## Machine Learning Pipeline

The model uses:

* Polynomial Features
* StandardScaler
* Gradient Boosting
* Cross Validation

The complete preprocessing and model pipeline is serialized using Joblib.

---

## Future Improvements

* Automated Retraining
* User Authentication
* Cloud Database Integration
* Email-Based Feedback Collection
* Advanced Analytics Dashboard

---

## Author

Daksh Kheni
