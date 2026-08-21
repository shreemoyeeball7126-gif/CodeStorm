import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range(
    start="2025-01-01",
    periods=250,
    freq="D"
)

data = []

for date in dates:

    day_of_week = date.dayofweek
    is_weekend = int(day_of_week >= 5)

    if is_weekend:
        attendance = np.random.randint(400, 651)
    else:
        attendance = np.random.randint(750, 1101)

    temperature = round(
        np.random.uniform(20, 35),
        1
    )

    holiday = int(
        np.random.choice(
            [0, 1],
            p=[0.93, 0.07]
        )
    )

    demand = (
        attendance * 0.90
        + temperature * 2
        - holiday * 200
        - is_weekend * 50
        + np.random.normal(0, 25)
    )

    meals_served = max(
        100,
        int(round(demand))
    )

    food_prepared = int(
        round(
            meals_served *
            np.random.uniform(1.05, 1.15)
        )
    )

    surplus_meals = max(
        0,
        food_prepared - meals_served
    )

    surplus_kg = round(
        surplus_meals * 0.10,
        2
    )

    data.append({
        "date": date.strftime("%Y-%m-%d"),
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "attendance": attendance,
        "temperature_c": temperature,
        "holiday": holiday,
        "food_prepared_meals": food_prepared,
        "meals_served": meals_served,
        "surplus_meals": surplus_meals,
        "surplus_kg": surplus_kg
    })

df = pd.DataFrame(data)

df.to_csv(
    "food_waste_250_days.csv",
    index=False
)

print("250-day dataset created!")
print("Rows:", len(df))
print("First date:", df["date"].iloc[0])
print("Last date:", df["date"].iloc[-1])