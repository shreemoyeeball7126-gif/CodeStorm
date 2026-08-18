import pandas as pd
import pickle


with open("demand_model.pkl", "rb") as f:
    model = pickle.load(f)


def predict_demand(day_of_week, weather, attendance_pct):

    input_data = pd.DataFrame([{
        "attendance_pct": attendance_pct,
        "day_of_week": day_of_week,
        "weather": weather
    }])


    input_encoded = pd.get_dummies(
        input_data,
        columns=["day_of_week", "weather"]
    )

    
    training_data = pd.read_csv("demand_data.csv")

    training_encoded = pd.get_dummies(
        training_data,
        columns=["day_of_week", "weather"]
    )

    X = training_encoded.drop(
        columns=["date", "meals_prepared", "meals_consumed"]
    )

    
    input_encoded = input_encoded.reindex(
        columns=X.columns,
        fill_value=0
    )

   
    prediction = model.predict(input_encoded)

    return round(prediction[0])


if __name__ == "__main__":

    predicted_demand = predict_demand(
        day_of_week="Monday",
        weather="Sunny",
        attendance_pct=80
    )

    print("Predicted demand:", predicted_demand, "meals")