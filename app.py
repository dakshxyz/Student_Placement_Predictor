import streamlit as st
from predict import predict_student
from db import save_prediction

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Student Placement Predictor",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
}

.sub-title {
    text-align: center;
    color: gray;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

.metric-container {
    padding: 1rem;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("🎓 Placement Predictor")

st.sidebar.info("""
### Features

✅ Placement Prediction

✅ Feedback Collection

✅ SQLite Database

✅ Retraining Pipeline

✅ Analytics Dashboard
""")

with st.sidebar.expander("Model Information"):
    st.write("""
    **Model:** Logistic Regression

    **Feature Engineering**
    - Polynomial Features
    - Standard Scaling

    **Validation Accuracy**
    - ~89%
    """)

# --------------------------------------------------
# Hero Section
# --------------------------------------------------

st.markdown(
    '<p class="main-title">🎓 Student Placement Predictor</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Predict a student\'s placement probability using Machine Learning.</p>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Input Form
# --------------------------------------------------

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📚 Academic Details")

        iq = st.number_input(
            "IQ",
            # min_value=50,
            # max_value=200,
            value=100
        )

        cgpa = st.number_input(
            "CGPA",
            # min_value=0.0,
            # max_value=10.0,
            value=7.0
        )

        academic = st.number_input(
            "Academic Performance",
            # min_value=0,
            # max_value=10,
            value=7
        )

        projects = st.number_input(
            "Projects Completed",
            # min_value=0,
            # max_value=20,
            value=3
        )

    with col2:

        st.subheader("🛠 Skills & Experience")

        internship = st.selectbox(
            "Internship Experience",
            ["No", "Yes"]
        )

        extra = st.number_input(
            "Extra Curricular Score",
            # min_value=0,
            # max_value=10,
            value=5
        )

        communication = st.number_input(
            "Communication Skills",
            # min_value=0,
            # max_value=10,
            value=7
        )

    submit = st.form_submit_button(
        "🚀 Predict Placement"
    )
    
    

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if submit:
    
    if not (50 <= iq <= 200):
        st.error("IQ must be between 50 and 200.")
        st.stop()
    
    if not (0 <= cgpa <= 10):
        st.error("CGPA must be between 0 and 10.")
        st.stop() 
        
    if not (0 <= academic <= 10):
        st.error("Academic Performance must be between 0 and 10.")
        st.stop()
        
    if not (0 <= extra <= 10):
        st.error("Extra Curricular Score must be between 0 and 10.")
        st.stop()
        
    if not (0 <= communication <= 10):
        st.error("Communication Skills must be between 0 and 10.")
        st.stop()
        
    if not (0 <= projects <= 20):
        st.error("Projects Completed must be between 0 and 20.")
        st.stop()


    internship_value = 1 if internship == "Yes" else 0
    prediction, probability = predict_student(
        iq,
        cgpa,
        academic,
        internship_value,
        extra,
        communication,
        projects
    )
    probability = min(probability, 0.9999)
    
    prediction = int(prediction)
    student_id = save_prediction(
        iq,
        cgpa,
        academic,
        internship_value,
        extra,
        communication,
        projects,
        prediction
    )
    
    st.divider()
    st.subheader("📈 Prediction Result")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(
            "Placement Probability",
            f"{probability * 100:.2f}%"
        )
        
    with col2:
        st.progress(float(probability))
        
    if prediction == 1:
            
        st.success(
            f"✅ Likely To Be Placed\n\nConfidence: {probability*100:.2f}%"
        )
    else:
        st.error(
            f"❌ Placement Seems Unlikely\n\nConfidence: {(1-probability)*100:.2f}%"
        )
        
        
    # Probability Interpretation
    if probability >= 0.80:
        st.success(
            "Strong placement prospects based on the provided profile."
        )
    elif probability >= 0.60:
        st.warning(
            "Moderate placement prospects. Improving projects and communication skills may help."
        )
    else:
        st.error(
            "Current placement prospects are relatively low. Consider improving academics, internships, and project work."
        )
    st.info(
        f"🆔 Reference ID: {student_id}\n\nSave this ID to submit feedback later."
    )