import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt




# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Meal Demand System",
    page_icon="🍱",
    layout="wide"
)
with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# ============================================================
# TITLE
# ============================================================

st.title("🍱 Smart Meal Demand & Surplus Management System")

st.write(
    "Forecast meal demand, reduce over-preparation, "
    "and safely redistribute eligible surplus food."
)

st.divider()

# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.header("📋 Input Information")

date = st.sidebar.date_input(
    "Select Date"
)

weather = st.sidebar.selectbox(
    "Weather",
    ["Sunny", "Cloudy", "Rainy"]
)

attendance = st.sidebar.number_input(
    "Expected Attendance (%)",
    min_value=0,
    max_value=100,
    value=80
)

meals_prepared = st.sidebar.number_input(
    "Meals Prepared",
    min_value=0,
    value=500
)

storage_time = st.sidebar.number_input(
    "Storage Time (hours)",
    min_value=0.0,
    value=2.0
)

storage_temp = st.sidebar.number_input(
    "Storage Temperature (°C)",
    value=4.0
)

predict_button = st.sidebar.button(
    "🔮 Predict Demand",
    type="primary"
)
def predict_demand(attendance, weather):
    """
    Temporary prediction function.

    Later this will call the trained ML model.
    """

    base_demand = attendance * 5

    if weather == "Rainy":
        base_demand *= 0.90

    elif weather == "Cloudy":
        base_demand *= 0.97

    return round(base_demand)
# ============================================================
# DEMO PREDICTION
# ============================================================

# Temporary value
# This will later come from Person 1 & 2's ML model.

predicted_demand = predict_demand(
    attendance,
    weather
)

# ============================================================
# SURPLUS CALCULATION
# ============================================================

surplus = meals_prepared - predicted_demand

if surplus < 0:
    surplus = 0


    st.header("🧠 Prediction Factors")

factor_col1, factor_col2, factor_col3 = st.columns(3)

with factor_col1:
    st.write("📅 Date")
    st.write(date)

with factor_col2:
    st.write("🌦️ Weather")
    st.write(weather)

with factor_col3:
    st.write("👥 Attendance")
    st.write(f"{attendance}%")

    

# ============================================================
# DASHBOARD METRICS
# ============================================================

st.header("📊 Today's Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Predicted Demand",
        f"{predicted_demand} meals"
    )

with col2:
    st.metric(
        "Meals Prepared",
        f"{meals_prepared} meals"
    )

with col3:
    st.metric(
        "Surplus",
        f"{surplus} meals"
    )

with col4:

    if surplus > 0:
        st.metric(
            "Status",
            "Surplus Detected"
        )
    else:
        st.metric(
            "Status",
            "No Surplus"
        )

st.divider()

# ============================================================
# SAFETY SECTION
# ============================================================

st.header("🛡️ Food Safety")

if storage_time <= 4:

    st.success(
        "✅ Food is currently marked as eligible for redistribution."
    )

    safety_status = "Eligible"

else:

    st.error(
        "❌ Food is marked as unsafe for redistribution."
    )

    safety_status = "Unsafe"

st.write(
    f"Storage time recorded: **{storage_time} hours**"
)

st.write(
    f"Storage temperature recorded: **{storage_temp} °C**"
)

st.divider()

# ============================================================
# DEMAND TREND
# ============================================================

st.header("📈 Predicted vs Actual Demand")

chart_data = pd.DataFrame(
    {
        "Day": [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ],
        "Actual Demand": [
            420,
            450,
            430,
            470,
            440,
            300,
            280
        ],
        "Predicted Demand": [
            425,
            445,
            435,
            460,
            445,
            310,
            290
        ]
    }
)

st.line_chart(
    chart_data.set_index("Day")
)

st.divider()

# ============================================================
# RECIPIENT MATCHING
# ============================================================

st.header("🤝 Surplus Recipient Matching")

# Temporary recipient data
# Person 3's matching algorithm will replace this later.

recipient_data = pd.DataFrame(
    {
        "Recipient": [
            "Community NGO",
            "Student Shelter",
            "Local Food Support Centre"
        ],
        "Capacity": [
            30,
            20,
            50
        ],
        "Distance (km)": [
            2.5,
            4.0,
            6.5
        ],
        "Priority": [
            1,
            2,
            3
        ]
    }
)

# Temporary greedy allocation

remaining_surplus = surplus

allocations = []

for index, row in recipient_data.iterrows():

    allocation = min(
        remaining_surplus,
        row["Capacity"]
    )

    allocations.append(allocation)

    remaining_surplus -= allocation

allocation_data = recipient_data.copy()

allocation_data["Meals Allocated"] = allocations

allocation_data["Status"] = allocation_data[
    "Meals Allocated"
].apply(
    lambda x: "Matched" if x > 0 else "Not Matched"
)

st.dataframe(
    allocation_data,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================================
# IMPACT METRICS
# ============================================================

st.header("🌱 Estimated Impact")

# Temporary assumptions
# Person 5 will provide the final agreed values.

meal_weight_kg = 0.45
meal_cost = 60
carbon_per_kg = 2.5

food_saved = surplus * meal_weight_kg
money_saved = surplus * meal_cost
carbon_saved = food_saved * carbon_per_kg

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Food Saved",
        f"{food_saved:.1f} kg"
    )

with col2:
    st.metric(
        "Estimated Money Saved",
        f"₹{money_saved:,.0f}"
    )

with col3:
    st.metric(
        "Estimated Carbon Avoided",
        f"{carbon_saved:.1f} kg CO₂e"
    )

st.divider()


st.caption(
    "SIH Prototype | Smart Meal Demand & Safe Surplus Redistribution"
)