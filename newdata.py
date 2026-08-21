import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def create_dataset(number_of_rows=500):

    np.random.seed(42)

    dates = pd.date_range(
        start="2025-01-01",
        periods=number_of_rows,
        freq="D"
    )

    data = []

    for date in dates:

        day_name = date.day_name()

        weekend = day_name in ["Saturday", "Sunday"]

        holiday = np.random.choice(
            ["Yes", "No"],
            p=[0.08, 0.92]
        )

        weather = np.random.choice(
            ["Normal", "Rainy", "Hot", "Cold"],
            p=[0.55, 0.20, 0.15, 0.10]
        )

        if holiday == "Yes":
            attendance = np.random.uniform(20, 50)

        elif weekend:
            attendance = np.random.uniform(45, 75)

        else:
            attendance = np.random.uniform(75, 98)

        if weather == "Rainy":
            attendance -= np.random.uniform(3, 10)

        elif weather == "Hot":
            attendance -= np.random.uniform(1, 5)

        elif weather == "Cold":
            attendance -= np.random.uniform(0, 3)

        attendance = max(10, min(100, attendance))

        event = np.random.choice(
            ["Yes", "No"],
            p=[0.12, 0.88]
        )

        if event == "Yes":
            attendance += np.random.uniform(2, 8)

        attendance = min(100, attendance)

        exam_day = np.random.choice(
            ["Yes", "No"],
            p=[0.10, 0.90]
        )

        meal_type = np.random.choice(
            ["Breakfast", "Lunch", "Dinner"],
            p=[0.25, 0.50, 0.25]
        )

        if meal_type == "Breakfast":
            base_demand = 450

        elif meal_type == "Lunch":
            base_demand = 700

        else:
            base_demand = 600

        demand = base_demand * (attendance / 100)

        if day_name == "Monday":
            demand += 20

        elif day_name == "Friday":
            demand -= 15

        elif weekend:
            demand -= 80

        if weather == "Rainy":
            demand -= 35

        elif weather == "Hot":
            demand -= 20

        elif weather == "Cold":
            demand -= 10

        if event == "Yes":
            demand += 45

        if exam_day == "Yes":
            demand -= 25

        if holiday == "Yes":
            demand -= 100

        noise = np.random.normal(0, 20)

        demand += noise

        demand = max(50, round(demand))

        data.append([
            date,
            day_name,
            weather,
            round(attendance, 2),
            holiday,
            event,
            exam_day,
            meal_type,
            demand
        ])

    df = pd.DataFrame(
        data,
        columns=[
            "date",
            "day_of_week",
            "weather",
            "attendance_pct",
            "holiday",
            "event",
            "exam_day",
            "meal_type",
            "meals_consumed"
        ]
    )

    return df


print("\nCreating realistic campus food demand dataset...")

df = create_dataset(500)

df.to_csv("demand_data.csv", index=False)

print("Dataset saved as demand_data.csv")

print("\nFirst 5 rows:")
print(df.head())

print("\nChecking missing values:")

print(df.isnull().sum())

df = df.drop_duplicates()

df["attendance_pct"] = df["attendance_pct"].clip(0, 100)

df["meals_consumed"] = df["meals_consumed"].clip(lower=0)

print("\nDataset after cleaning:")
print(df.shape)

print("\nDataset statistics:")
print(df.describe(include="all"))

print("\nAverage demand by meal type:")

meal_summary = df.groupby("meal_type")["meals_consumed"].mean()

print(meal_summary)

print("\nAverage demand by weather:")

weather_summary = df.groupby("weather")["meals_consumed"].mean()

print(weather_summary)

print("\nAverage demand by day:")

day_summary = df.groupby("day_of_week")["meals_consumed"].mean()

print(day_summary)

plt.figure(figsize=(10, 5))

plt.plot(
    df["date"],
    df["meals_consumed"],
    linewidth=1
)

plt.title("Campus Meal Demand Over Time")
plt.xlabel("Date")
plt.ylabel("Meals Consumed")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("demand_pattern.png")

plt.show()

features = [
    "day_of_week",
    "weather",
    "attendance_pct",
    "holiday",
    "event",
    "exam_day",
    "meal_type"
]

target = "meals_consumed"

X = df[features]

y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

categorical_features = [
    "day_of_week",
    "weather",
    "holiday",
    "event",
    "exam_day",
    "meal_type"
]

numerical_features = [
    "attendance_pct"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),

        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

linear_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            LinearRegression()
        )
    ]
)

print("\nTraining Linear Regression...")

linear_model.fit(
    X_train,
    y_train
)

linear_predictions = linear_model.predict(X_test)

linear_mae = mean_absolute_error(
    y_test,
    linear_predictions
)

linear_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        linear_predictions
    )
)

linear_r2 = r2_score(
    y_test,
    linear_predictions
)

print("\n==============================")
print("LINEAR REGRESSION RESULTS")
print("==============================")

print("MAE :", round(linear_mae, 2))
print("RMSE:", round(linear_rmse, 2))
print("R2  :", round(linear_r2, 3))

tree_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            DecisionTreeRegressor(
                max_depth=6,
                min_samples_leaf=5,
                random_state=42
            )
        )
    ]
)

print("\nTraining Decision Tree...")

tree_model.fit(
    X_train,
    y_train
)

tree_predictions = tree_model.predict(X_test)

tree_mae = mean_absolute_error(
    y_test,
    tree_predictions
)

tree_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        tree_predictions
    )
)

tree_r2 = r2_score(
    y_test,
    tree_predictions
)

print("\n==============================")
print("DECISION TREE RESULTS")
print("==============================")

print("MAE :", round(tree_mae, 2))
print("RMSE:", round(tree_rmse, 2))
print("R2  :", round(tree_r2, 3))

print("\n===================================")
print("MODEL COMPARISON")
print("===================================")

print(
    f"Linear Regression MAE : {linear_mae:.2f}"
)

print(
    f"Decision Tree MAE     : {tree_mae:.2f}"
)

if tree_mae < linear_mae:

    best_model = tree_model
    best_model_name = "Decision Tree"
    best_mae = tree_mae

else:

    best_model = linear_model
    best_model_name = "Linear Regression"
    best_mae = linear_mae

print("\nBest Model:", best_model_name)

print(
    f"Best MAE: {best_mae:.2f} meals"
)

model_filename = "best_demand_model.pkl"

joblib.dump(
    best_model,
    model_filename
)

print(
    f"\nBest model saved as: {model_filename}"
)

results = pd.DataFrame({

    "Model": [
        "Linear Regression",
        "Decision Tree"
    ],

    "MAE": [
        linear_mae,
        tree_mae
    ],

    "RMSE": [
        linear_rmse,
        tree_rmse
    ],

    "R2": [
        linear_r2,
        tree_r2
    ]
})

results.to_csv(
    "model_comparison.csv",
    index=False
)

print(
    "Model comparison saved as model_comparison.csv"
)


def predict_meal_demand(
    date,
    weather,
    attendance_pct,
    holiday,
    event,
    exam_day,
    meal_type
):

    date = pd.to_datetime(date)

    day_of_week = date.day_name()

    input_data = pd.DataFrame({

        "day_of_week": [day_of_week],

        "weather": [weather],

        "attendance_pct": [
            attendance_pct
        ],

        "holiday": [holiday],

        "event": [event],

        "exam_day": [exam_day],

        "meal_type": [meal_type]

    })

    prediction = best_model.predict(
        input_data
    )[0]

    prediction = max(
        0,
        round(prediction)
    )

    preparation_buffer = 0.03

    recommended_preparation = round(
        prediction * (1 + preparation_buffer)
    )

    return prediction, recommended_preparation


print("\n===================================")
print("SAMPLE DEMAND PREDICTION")
print("===================================")

predicted_demand, recommended_preparation = predict_meal_demand(

    date="2026-09-15",

    weather="Normal",

    attendance_pct=90,

    holiday="No",

    event="No",

    exam_day="No",

    meal_type="Lunch"
)

print(
    "Predicted demand =",
    predicted_demand,
    "meals"
)

print(
    "Recommended preparation =",
    recommended_preparation,
    "meals"
)

loaded_model = joblib.load(
    "best_demand_model.pkl"
)

print(
    "\nSaved model successfully loaded."
)

print("\n===================================")
print("ML MODULE COMPLETED")
print("===================================")

print("Dataset              : demand_data.csv")
print("Demand graph         : demand_pattern.png")
print("Model comparison     : model_comparison.csv")
print("Best trained model   : best_demand_model.pkl")
print("Selected model       :", best_model_name)
print("Final MAE            :", round(best_mae, 2))
print("===================================")
