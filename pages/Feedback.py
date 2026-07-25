import streamlit as st
from db import update_actual_placement

st.title("Placement Feedback")

student_id = st.number_input(
    "Student ID",
    min_value=1,
    step=1
)

actual = st.selectbox(
    "Actual Placement Result",
    ["Placed", "Not Placed"]
)

if st.button("Submit Feedback"):

    actual_value = 1 if actual == "Placed" else 0

    update_actual_placement(
        student_id,
        actual_value
    )

    st.success("Feedback saved.")
