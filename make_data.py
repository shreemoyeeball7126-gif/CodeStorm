import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range(start="2026-01-01", periods=250, freq="D")

day_of_week = dates.day_name()


weather_options = ["Sunny", "Cloudy", "Rainy"]
weather = np.random.choice(weather_options, size=250, p=[0.6, 0.25, 0.15])

attendance_pct = np.random.normal(loc=80, scale=10, size=250)
attendance_pct = np.clip(attendance_pct, 40, 100)

base_demand = 500
meals_consumed = []

for i in range(250):
    demand = base_demand

    if day_of_week[i] in ["Saturday", "Sunday"]:
        demand = demand * 0.7

    if weather[i] == "Rainy":
        demand = demand * 0.85

    demand = demand * (attendance_pct[i] / 80)

    demand = demand + np.random.normal(0, 20)

    if demand < 0:
        demand = 0

    meals_consumed.append(demand)

meals_consumed = np.array(meals_consumed).round().astype(int)

overprep_factor = np.random.uniform(1.05, 1.20, size=250)
meals_prepared = (meals_consumed * overprep_factor).round().astype(int)

df = pd.DataFrame({
    "date": dates,
    "day_of_week": day_of_week,
    "weather": weather,
    "attendance_pct": attendance_pct.round(1),
    "meals_prepared": meals_prepared,
    "meals_consumed": meals_consumed,
})

df.to_csv("demand_data.csv", index=False)

print("Done! Created demand_data.csv with 250 rows.")
pd.set_option('display.max_rows', None)
print(df)