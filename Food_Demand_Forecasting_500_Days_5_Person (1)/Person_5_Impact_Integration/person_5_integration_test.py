from pathlib import Path
import pickle
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Person_3_Surplus_Donation"))
sys.path.insert(0, str(ROOT / "Person_5_Impact_Integration"))

from person_3_surplus_donation import (
    recommended_preparation,
    calculate_surplus,
    donation_recommendation
)
from person_5_impact import calculate_impact

df = pd.read_csv(ROOT / "Person_1_Data" / "demand_data.csv")

assert len(df) == 500
assert df["attendance_pct"].between(0, 100).all()
assert (df["meals_consumed"] <= df["meals_prepared"]).all()
print("PASS: 500-day dataset")

with open(ROOT / "Person_2_ML" / "demand_model.pkl", "rb") as f:
    bundle = pickle.load(f)

sample = pd.DataFrame([{
    "day_of_week": "Monday",
    "is_weekend": 0,
    "weather": "Sunny",
    "exam_day": 0,
    "event": "None",
    "attendance_pct": 86,
    "lag_1_consumed": 400,
    "rolling_7_consumed": 395
}])

prediction = max(0, float(bundle["model"].predict(sample)[0]))
recommended = recommended_preparation(prediction)
surplus = calculate_surplus(recommended, prediction)

assert prediction >= 0
assert recommended >= round(prediction)
assert surplus >= 0

print("PASS: ML + minimal surplus")

allocations = donation_recommendation(surplus)
assert isinstance(allocations, list)
print("PASS: Donation recommendation")

impact = calculate_impact(surplus)
assert impact["meals_redistributed"] >= 0
print("PASS: Impact calculation")

assert recommended_preparation(438) == 455
assert calculate_surplus(455, 438) == 17
print("PASS: 438 -> 455 -> 17 example")

print("ALL TESTS PASSED.")
