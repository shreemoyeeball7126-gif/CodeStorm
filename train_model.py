import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv("demand_data.csv")

df_encoded = pd.get_dummies(df, columns=["day_of_week", "weather"])
print(df_encoded.head())

X = df_encoded.drop(columns=["date", "meals_prepared", "meals_consumed"])
y = df_encoded["meals_consumed"]

print(X.head())
print(y.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
model = LinearRegression()
model.fit(X_train, y_train)

print("Model trained!")
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5

print("Mean Absolute Error:", mae)
print("Root Mean Squared Error:", rmse)
import pickle

with open("demand_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as demand_model.pkl")