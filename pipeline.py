import pandas as pd
from predict import predict_demand as ml_predict_demand
from surplus_logic import process_surplus, recipients
from impact import calculate_impact

DATA_FILE = (
    "food_waste_250_days.csv"
)

AVERAGE_MEAL_WEIGHT_KG = 0.10


def load_data():

    df = pd.read_csv(
        DATA_FILE
    )

    # Convert date column

    df["date"] = pd.to_datetime(
        df["date"]
    )


    return df



def get_date_data(
    df,
    selected_date
):

    selected_date = pd.to_datetime(
        selected_date
    )


    rows = df[
        df["date"] == selected_date
    ]


    if rows.empty:

        raise ValueError(
            "No data available for this date."
        )


    return rows.iloc[0]


def predict_demand(row):
    """
    Convert the 250-day dataset fields into the
    feature format expected by our trained ML model.
    """

    temperature = row["temperature_c"]

    if temperature < 20:
        weather = "Cloudy"
    elif temperature >= 30:
        weather = "Sunny"
    else:
        weather = "Rainy"

    attendance = float(row["attendance"])

    # Convert values like 852 -> 85.2%
    if attendance > 100:
        attendance = attendance / 10

    predicted = ml_predict_demand(
        day_of_week=row["day_of_week"],
        weather=weather,
        attendance_pct=attendance
    )

    return predicted



def calculate_surplus(
    food_prepared,
    predicted_demand
):

    surplus_meals = (
        food_prepared
        - predicted_demand
    )


    # Surplus cannot be negative

    surplus_meals = max(
        0,
        surplus_meals
    )


    return surplus_meals




def convert_to_kg(
    surplus_meals
):

    surplus_kg = (
        surplus_meals
        * AVERAGE_MEAL_WEIGHT_KG
    )


    return round(
        surplus_kg,
        2
    )



def run_pipeline(
    selected_date,
    storage_time,
    temperature
):
    df = load_data()
    row = get_date_data(
        df,
        selected_date
    )

    food_prepared = int(
        row[
            "food_prepared_meals"
        ]
    )


   

    predicted_demand = predict_demand(
        row
    )


    
    surplus_meals = calculate_surplus(

        food_prepared,

        predicted_demand
    )


   

    surplus_kg = convert_to_kg(
        surplus_meals
    )


    impact = calculate_impact(
        surplus_kg
    )


   

    return {

        "date":
            str(
                row["date"].date()
            ),

       "attendance":
    float(row["attendance"]) / 10
    if float(row["attendance"]) > 100
    else float(row["attendance"]),

        "temperature":
            float(
                row["temperature_c"]
            ),

        "food_prepared":
            food_prepared,

        "predicted_demand":
            predicted_demand,

        "surplus_meals":
            surplus_meals,

        "surplus_kg":
            surplus_kg,

        "food_saved_kg":
            impact[
                "food_saved_kg"
            ],

        "money_saved":
            impact[
                "money_saved"
            ],

        "carbon_saved_kg":
            impact[
                "carbon_saved_kg"
            ]
    }




if __name__ == "__main__":

    result = run_pipeline(
        "2025-01-01"
    )


    print()
    print(
        "================================"
    )

    print(
        "       FOODWISE PIPELINE"
    )

    print(
        "================================"
    )

    print()


    for key, value in result.items():

        print(
            f"{key}: {value}"
        )