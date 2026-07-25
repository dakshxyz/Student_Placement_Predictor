import pandas as pd
import streamlit as st

from db import (
    get_total_predictions,
    get_predicted_placed,
    get_predicted_not_placed,
    get_feedback_received,
    get_pending_feedback,
    get_live_accuracy,
    get_recent_predictions
)

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard")

# -------------------------
# KPI Metrics
# -------------------------

total_predictions = get_total_predictions()
placed_predictions = get_predicted_placed()
not_placed_predictions = get_predicted_not_placed()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Predictions",
        total_predictions
    )

with col2:
    st.metric(
        "Placed Predictions",
        placed_predictions
    )

with col3:
    st.metric(
        "Not Placed Predictions",
        not_placed_predictions
    )

# -------------------------
# Feedback Metrics
# -------------------------

feedback_received = get_feedback_received()
pending_feedback = get_pending_feedback()
accuracy = get_live_accuracy()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Feedback Received",
        feedback_received
    )

with col2:
    st.metric(
        "Pending Feedback",
        pending_feedback
    )

with col3:

    if accuracy is None:
        st.metric(
            "Live Accuracy",
            "N/A"
        )
    else:
        st.metric(
            "Live Accuracy",
            f"{accuracy*100:.2f}%"
        )

# -------------------------
# Prediction Distribution
# -------------------------

st.subheader("Prediction Distribution")

chart_data = pd.DataFrame({
    "Category": ["Placed", "Not Placed"],
    "Count": [
        placed_predictions,
        not_placed_predictions
    ]
})

st.bar_chart(
    chart_data.set_index("Category")
)

st.subheader("Placement Prediction Ratio")

placed_ratio = (
    placed_predictions /
    total_predictions
    if total_predictions > 0
    else 0
)

st.progress(placed_ratio)

st.write(
    f"{placed_ratio*100:.2f}% of predictions are positive."
)

# -------------------------
# Recent Predictions
# -------------------------

st.subheader("Recent Predictions")

recent_df = get_recent_predictions()

st.dataframe(
    recent_df,
    use_container_width=True
)
