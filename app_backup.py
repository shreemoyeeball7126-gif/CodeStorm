import streamlit as st

from pipeline import (
    load_data,
    run_pipeline
)


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(

    page_title="FoodWise",

    page_icon="🍽️",

    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title(
    "🍽️ FoodWise"
)

st.subheader(
    "Smart Food Demand Prediction "
    "and Waste Reduction"
)


st.write(
    "Select a date to see the predicted "
    "food demand, surplus food and "
    "environmental impact."
)


# ==========================================
# LOAD DATA
# ==========================================

df = load_data()


# ==========================================
# DATE SELECTOR
# ==========================================

selected_date = st.date_input(

    "📅 Select a Date",

    value=df[
        "date"
    ].min().date(),

    min_value=df[
        "date"
    ].min().date(),

    max_value=df[
        "date"
    ].max().date()
)


# ==========================================
# RUN PIPELINE
# ==========================================

result = run_pipeline(
    selected_date
)


# ==========================================
# PREDICTION SECTION
# ==========================================

st.header(
    "📊 Demand Prediction"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Attendance",
        result["attendance"]
    )


with col2:

    st.metric(
        "Food Prepared",
        f"{result['food_prepared']} meals"
    )


with col3:

    st.metric(
        "Predicted Demand",
        f"{result['predicted_demand']} meals"
    )


# ==========================================
# SURPLUS SECTION
# ==========================================

st.header(
    "🥘 Surplus Food"
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Surplus Meals",
        result["surplus_meals"]
    )


with col2:

    st.metric(
        "Surplus Food",
        f"{result['surplus_kg']:.2f} kg"
    )


# ==========================================
# IMPACT SECTION
# ==========================================

st.header(
    "🌱 Environmental & Financial Impact"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(

        "🍚 Food Saved",

        f"{result['food_saved_kg']:.2f} kg"
    )


with col2:

    st.metric(

        "💰 Money Saved",

        f"₹{result['money_saved']:,.2f}"
    )


with col3:

    st.metric(

        "🌍 Carbon Avoided",

        f"{result['carbon_saved_kg']:.2f} kg CO₂e"
    )


# ==========================================
# CALCULATION DETAILS
# ==========================================

st.header(
    "🧮 Calculation Details"
)


st.write(
    f"""
    **Food prepared:** 
    {result['food_prepared']} meals

    **Predicted demand:** 
    {result['predicted_demand']} meals

    **Surplus meals:** 
    {result['food_prepared']} − 
    {result['predicted_demand']} = 
    {result['surplus_meals']} meals

    **Surplus food:** 
    {result['surplus_meals']} × 0.10 kg = 
    {result['surplus_kg']} kg
    """
)


# ==========================================
# 250-DAY DATA
# ==========================================

st.header(
    "📈 250-Day Food Data"
)


chart_data = df[
    [
        "date",
        "food_prepared_meals",
        "meals_served"
    ]
].copy()


chart_data = chart_data.set_index(
    "date"
)


chart_data.columns = [

    "Food Prepared",

    "Meals Served"
]


st.line_chart(
    chart_data
)


# ==========================================
# FOOTER
# ==========================================

st.divider()


st.caption(
    "FoodWise — Reducing food waste "
    "through smarter demand prediction."
)