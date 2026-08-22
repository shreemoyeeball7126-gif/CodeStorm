# PERSON 4 — Streamlit dashboard.
# Run from the project root:
# streamlit run Person_4_Dashboard/app.py

from pathlib import Path
import pickle
import sys
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Person_3_Surplus_Donation"))

from person_3_surplus_donation import (
    recommended_preparation,
    calculate_surplus,
    donation_recommendation
)

DATA_FILE = ROOT / "Person_1_Data" / "demand_data.csv"
MODEL_FILE = ROOT / "Person_2_ML" / "demand_model.pkl"

st.set_page_config(
    page_title="Food Demand Forecasting",
    page_icon="🍱",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df["attendance_pct"] = df["attendance_pct"].clip(0, 100)
    return df

@st.cache_resource
def load_model():
    with open(MODEL_FILE, "rb") as f:
        return pickle.load(f)

df = load_data()
bundle = load_model()
model = bundle["model"]

st.title("🍱 Food Demand Forecasting & Surplus Redistribution")
st.caption("500 days of historical data • minimal preparation buffer")

st.sidebar.header("Forecast Inputs")

selected_date = st.sidebar.date_input(
    "Date",
    value=df["date"].max().date(),
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date()
)

weather = st.sidebar.selectbox(
    "Weather", ["Sunny", "Cloudy", "Rainy", "Hot"]
)

attendance = st.sidebar.slider(
    "Attendance (%)", 0, 100, 86, 1
)

exam_day = st.sidebar.checkbox("Exam Day", False)

event = st.sidebar.selectbox(
    "Event",
    ["None", "Festival", "Sports Event", "Cultural Event", "Workshop"]
)

timestamp = pd.Timestamp(selected_date)
history = df[df["date"] < timestamp].sort_values("date")

if history.empty:
    lag_1 = float(df["meals_consumed"].mean())
    rolling_7 = lag_1
else:
    lag_1 = float(history.iloc[-1]["meals_consumed"])
    rolling_7 = float(history["meals_consumed"].tail(7).mean())

input_df = pd.DataFrame([{
    "day_of_week": timestamp.day_name(),
    "is_weekend": int(timestamp.weekday() >= 5),
    "weather": weather,
    "exam_day": int(exam_day),
    "event": event,
    "attendance_pct": float(np.clip(attendance, 0, 100)),
    "lag_1_consumed": lag_1,
    "rolling_7_consumed": rolling_7
}])

predicted = max(0, float(model.predict(input_df)[0]))
recommended = recommended_preparation(predicted)
surplus = calculate_surplus(recommended, predicted)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Predicted Demand", f"{predicted:.0f} meals")
c2.metric("Recommended Preparation", f"{recommended} meals")
c3.metric("Expected Surplus", f"{surplus} meals")
c4.metric("Attendance", f"{attendance}%")

st.info(
    "Only a 3.8% preparation buffer is used. "
    "Example: 438 predicted → 455 recommended → 17 surplus."
)

st.subheader("Historical Demand")
st.line_chart(
    df.set_index("date")[["meals_prepared", "meals_consumed"]].tail(60)
)

st.subheader("Recommended Donation Destination")

allocations = donation_recommendation(surplus)

if surplus == 0:
    st.success("No surplus is expected.")
elif allocations:
    donation_df = pd.DataFrame(allocations)
    st.dataframe(
        donation_df,
        use_container_width=True,
        hide_index=True
    )
    assigned = int(donation_df["recommended_meals"].sum())
    st.success(
        f"{assigned} of {surplus} expected surplus meals have a recommended destination."
    )
else:
    st.warning("No verified recipient is currently available.")

with st.expander("Data Quality Checks"):
    bad_attendance = int((~df["attendance_pct"].between(0, 100)).sum())
    bad_meals = int(
        (df["meals_consumed"] > df["meals_prepared"]).sum()
    )
    st.write("Attendance above 100%:", bad_attendance)
    st.write("Consumed > Prepared:", bad_meals)

    if bad_attendance == 0 and bad_meals == 0:
        st.success("All core data checks passed.")
