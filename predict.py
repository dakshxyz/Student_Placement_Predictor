import joblib
import pandas as pd

model = joblib.load('placement_predictor.pkl')

def predict_student(
    iq,
    cgpa,
    academic,
    internship,
    extra,
    communication,
    projects
):

    df = pd.DataFrame({
        'IQ':[iq],
        'CGPA':[cgpa],
        'Academic_Performance':[academic],
        'Internship_Experience':[internship],
        'Extra_Curricular_Score':[extra],
        'Communication_Skills':[communication],
        'Projects_Completed':[projects]
    })

    prediction = int(model.predict(df)[0])
    probability = model.predict_proba(df)[0][1]

    return prediction, probability