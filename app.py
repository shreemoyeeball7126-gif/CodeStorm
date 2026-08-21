import streamlit as st
from pipeline import load_data, run_pipeline

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="FoodWise",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🍽️ FoodWise")
st.subheader("Smart Meal Demand & Surplus Management")

st.write(
    "Forecast meal demand, detect surplus, verify food safety, "
    "and estimate environmental and financial impact."
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data()

# -----------------------------
# INPUTS
# -----------------------------
st.sidebar.header("Analysis Controls")

selected_date = st.sidebar.date_input(
    "Select Date",
    value=df["date"].min().date(),
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date(),
    key="analysis_date"
)

storage_time = st.sidebar.number_input(
    "Storage Time (hours)",
    min_value=0.0,
    value=2.0,
    step=0.5
)

temperature = st.sidebar.number_input(
    "Storage Temperature (°C)",
    value=4.0,
    step=0.5
)

run = st.sidebar.button(
    "Run FoodWise Analysis"
)

# -----------------------------
# RUN ANALYSIS
# -----------------------------
if run:

    result = run_pipeline(
        selected_date,
        storage_time=storage_time,
        temperature=temperature
    )

    # -------------------------
    # DEMAND
    # -------------------------
    st.header("📊 Demand Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Attendance",
            f"{result['attendance']:.1f}%"
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

    # -------------------------
    # SURPLUS
    # -------------------------
    st.header("🥘 Surplus Detection")

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

    # -------------------------
    # IMPACT
    # -------------------------
    st.header("🌱 Estimated Impact")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Food Saved",
            f"{result['food_saved_kg']:.2f} kg"
        )

    with col2:
        st.metric(
            "Money Saved",
            f"₹{result['money_saved']:,.0f}"
        )

    with col3:
        st.metric(
            "Carbon Avoided",
            f"{result['carbon_saved_kg']:.2f} kg CO₂e"
        )

    # -------------------------
    # DETAILS
    # -------------------------
    st.header("🔍 Analysis Details")

    st.write(f"Selected date: {selected_date}")
    st.write(f"Storage time: {storage_time} hours")
    st.write(f"Storage temperature: {temperature} °C")

    st.success("FoodWise analysis completed successfully.")

else:

    st.info(
        "Select a date and storage conditions from the sidebar, "
        "then click Run FoodWise Analysis."
    )

# -----------------------------
# HISTORICAL DATA
# -----------------------------
st.header("📈 Historical Meal Data")

chart = df[
    [
        "date",
        "food_prepared_meals",
        "meals_served"
    ]
].copy()

chart = chart.set_index("date")

chart.columns = [
    "Food Prepared",
    "Meals Served"
]

st.line_chart(chart)

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "FoodWise | Smarter food planning, safer redistribution, less waste."
)