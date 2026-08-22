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
    donation_recommendation,
    preparation_buffer,
    storage_safety_guidance,
)

DATA_FILE = ROOT / "Person_1_Data" / "demand_data.csv"
MODEL_FILE = ROOT / "Person_2_ML" / "demand_model.pkl"

st.set_page_config(
    page_title="Mess Hall Planning Board",
    page_icon="🌾",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Visual identity — "harvest board": deep pine green + wheat gold on a pale
# sage-cream ground, Fraunces for display type, Inter for data and body text.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --forest: #2B5233;
    --forest-dark: #1B3A22;
    --wheat: #D9A441;
    --wheat-dark: #B9822B;
    --clay: #C1443C;
    --cream: #F3F5EC;
    --card: #FFFEFA;
    --ink: #22301F;
    --muted: #6B7A63;
    color-scheme: light !important;
}

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; color: var(--ink); color-scheme: light !important; }

/* Force every widget to light styling regardless of the viewer's OS/browser
   dark-mode preference, so it never falls back to dark backgrounds. */
.stApp, .stApp * {
    color-scheme: light !important;
}
/* Selectbox control (the closed pill) — target every nesting level since
   BaseWeb wraps the value a few divs deep. */
[data-testid="stSelectbox"] div[data-baseweb="select"],
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stSelectbox"] div[data-baseweb="select"] div {
    background-color: #FFFFFF !important;
    color: #22301F !important;
    border-color: rgba(34, 48, 31, 0.35) !important;
}
[data-testid="stSelectbox"] svg { fill: #22301F !important; }

/* Dropdown option list (the open popover) */
div[data-baseweb="popover"],
div[data-baseweb="popover"] *,
ul[role="listbox"],
li[role="option"] {
    background-color: #FFFFFF !important;
    color: #22301F !important;
}
li[role="option"]:hover, li[role="option"][aria-selected="true"] {
    background-color: #F0EEE3 !important;
}

/* Date input field */
[data-testid="stDateInput"] input,
[data-testid="stDateInput"] div {
    background-color: #FFFFFF !important;
    color: #22301F !important;
}
.stApp { background-color: var(--cream); }

/* Hero banner */
.board-hero {
    background: linear-gradient(135deg, var(--forest) 0%, var(--forest-dark) 100%);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 6px 18px rgba(27, 58, 34, 0.25);
}
.board-kicker {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--wheat);
    margin-bottom: 6px;
}
.board-title {
    font-family: 'Fraunces', serif;
    font-weight: 600 !important;
    font-size: 2.8rem !important;
    line-height: 1.05 !important;
    margin: 0 0 14px 0 !important;
    width: 100%;
    word-wrap: break-word;
    word-break: break-word;
    color: #FFFEFA !important;
}
[data-testid="stMarkdownContainer"] p.board-title {
    font-size: 2.8rem !important;
    line-height: 1.05 !important;
    color: #FFFEFA !important;
}
.board-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: #D9E2D3;
    margin: 0;
}

/* Condition badges */
.badge-row { margin: 14px 0 4px 0; }
.badge {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 999px;
    margin-right: 8px;
    margin-bottom: 6px;
}
.badge-active {
    background: var(--wheat);
    color: var(--forest-dark);
}
.badge-inactive {
    background: rgba(255,255,255,0.10);
    color: #D9E2D3;
    border: 1px solid rgba(255,255,255,0.25);
}

/* Section headers */
.section-kicker {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--wheat-dark);
    margin: 26px 0 2px 0;
}
.section-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.5rem;
    color: var(--forest-dark);
    margin: 0 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--wheat);
}

/* Metric cards */
.card-row { display: flex; gap: 14px; margin-bottom: 6px; flex-wrap: wrap; }
.metric-card {
    background: var(--card);
    border: 1px solid rgba(43, 82, 51, 0.12);
    border-left: 5px solid var(--forest);
    border-radius: 12px;
    padding: 14px 18px;
    flex: 1;
    min-width: 150px;
    box-shadow: 0 2px 6px rgba(34, 48, 31, 0.06);
}
.metric-card.gold { border-left-color: var(--wheat-dark); }
.metric-card.clay { border-left-color: var(--clay); }
.metric-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #000000;
}
.metric-value {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.9rem;
    color: var(--ink);
    line-height: 1.3;
}

/* Buffer note */
.buffer-note {
    background: rgba(217, 164, 65, 0.14);
    border: 1px solid rgba(217, 164, 65, 0.4);
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 0.86rem;
    color: var(--forest-dark);
    margin: 10px 0 4px 0;
}

section[data-testid="stSidebar"] {
    background-color: var(--forest-dark);
}
/* Only recolor labels/headings/plain text on the dark sidebar background —
   never the value text inside the white input/select/date boxes, or it
   becomes unreadable (light text on a white field). */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stMarkdown p {
    color: #F3F5EC !important;
}
/* Widget value text (date input, selectbox, slider readout) keeps normal
   dark text since it sits on a white/near-white field. */
section[data-testid="stSidebar"] [data-baseweb="select"] *,
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] [data-testid="stDateInput"] * {
    color: #22301F !important;
}
</style>
""", unsafe_allow_html=True)


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

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="board-hero">
    <div class="board-kicker">🌾 Mess Hall Planning Board</div>
    <p class="board-title">Food Demand Forecasting &amp; Surplus Redistribution</p>
    <p class="board-sub">500 days of dining-hall history, forecast ahead, and a minimal-surplus prep plan for every day.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🧾 Forecast Inputs")

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
    "Attendance (%)", 0, 100, 78, 1
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
recommended = recommended_preparation(predicted, int(exam_day), event)
surplus = calculate_surplus(recommended, predicted)
buffer_pct = preparation_buffer(int(exam_day), event) * 100

# ---------------------------------------------------------------------------
# Today's board — condition badges
# ---------------------------------------------------------------------------
def badge(label, active):
    cls = "badge badge-active" if active else "badge badge-inactive"
    return f'<span class="{cls}">{label}</span>'

badges_html = "".join([
    badge("📖 Exam Day", bool(exam_day)),
    badge(f"🎉 {event}" if event != "None" else "🎉 No Event", event != "None"),
    badge(f"☀️ Sunny" if weather == "Sunny" else f"🌤️ {weather}", weather == "Sunny"),
])
st.markdown(f'<div class="badge-row">{badges_html}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Metric cards
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="card-row">
    <div class="metric-card">
        <div class="metric-label">Predicted Demand</div>
        <div class="metric-value">{predicted:.0f}</div>
    </div>
    <div class="metric-card gold">
        <div class="metric-label">Recommended Preparation</div>
        <div class="metric-value">{recommended}</div>
    </div>
    <div class="metric-card clay">
        <div class="metric-label">Expected Surplus</div>
        <div class="metric-value">{surplus}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Attendance</div>
        <div class="metric-value">{attendance}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="buffer-note">
🌾 Preparation buffer applied today: <strong>{buffer_pct:.1f}%</strong>
&nbsp;—&nbsp; buffer scales between 3.8%–4.5% depending on exam days and events, keeping surplus as small as possible.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Historical demand
# ---------------------------------------------------------------------------
st.markdown('<div class="section-kicker">Trend</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Historical Demand</div>', unsafe_allow_html=True)
st.line_chart(
    df.set_index("date")[["meals_prepared", "meals_consumed"]].tail(60),
    color=["#D9A441", "#2B5233"]
)

# ---------------------------------------------------------------------------
# Donations
# ---------------------------------------------------------------------------
st.markdown('<div class="section-kicker">Redistribution</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Recommended Donation Destinations</div>', unsafe_allow_html=True)

allocations = donation_recommendation(surplus)

if surplus == 0:
    st.success("No surplus is expected — nothing to donate today.")
elif allocations:
    donation_df = pd.DataFrame(allocations)[
        ["recipient", "type", "recommended_meals", "capacity", "distance_km", "priority"]
    ]
    st.dataframe(
        donation_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "recipient": st.column_config.TextColumn("Recipient"),
            "type": st.column_config.TextColumn("Type"),
            "recommended_meals": st.column_config.NumberColumn("Recommended Meals"),
            "capacity": st.column_config.NumberColumn("Capacity"),
            "distance_km": st.column_config.NumberColumn("Distance", format="%.1f km"),
            "priority": st.column_config.ProgressColumn(
                "Priority", min_value=0, max_value=5, format="%d"
            ),
        }
    )
    assigned = int(donation_df["recommended_meals"].sum())
    st.success(
        f"🌾 {assigned} of {surplus} expected surplus meals have a recommended destination, "
        f"across {len(donation_df)} recipient{'s' if len(donation_df) != 1 else ''}."
    )
else:
    st.warning("No verified recipient is currently available.")

# ---------------------------------------------------------------------------
# Storage & food safety
# ---------------------------------------------------------------------------
st.markdown('<div class="section-kicker">Food Safety</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧊 Storage Guidance for Surplus</div>', unsafe_allow_html=True)

if surplus == 0:
    st.info("No surplus meals to store today.")
else:
    storage_df = pd.DataFrame(storage_safety_guidance(selected_date, surplus))
    st.dataframe(
        storage_df[[
            "storage_method", "storage_temperature", "max_storage_duration",
            "prepared_on", "safe_to_consume_until", "notes"
        ]],
        use_container_width=True,
        hide_index=True
    )
    st.markdown(
        "<p style='color:#000000; font-size:0.85rem;'>"
        "Distribute same-day whenever possible. If surplus can't be picked up "
        "immediately, refrigerate right away, and freeze anything that won't "
        "be collected within 3 days."
        "</p>",
        unsafe_allow_html=True
    )

with st.expander("📋 Data Overview"):
    st.write("Total days in dataset:", len(df))
    st.write("Date range:", df["date"].min().date(), "to", df["date"].max().date())
    st.write("Average attendance:", f'{df["attendance_pct"].mean():.1f}%')
    st.write("Average surplus per day:", f'{df["surplus_meals"].mean():.1f} meals')
