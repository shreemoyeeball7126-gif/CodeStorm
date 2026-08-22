import pandas as pd

df = pd.read_csv("demand_data.csv")

assert len(df) == 500
assert df["attendance_pct"].between(0, 100).all()
assert (df["meals_consumed"] <= df["meals_prepared"]).all()
assert (df["surplus_meals"] >= 0).all()

print("PASS: 500-day dataset")
print("Date:", df["date"].min(), "to", df["date"].max())
print("Attendance:", df["attendance_pct"].min(), "to", df["attendance_pct"].max())
