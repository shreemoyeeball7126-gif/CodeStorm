import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("demand_data.csv")
print(df.isnull().sum())
plt.plot(df["date"], df["meals_consumed"])
plt.xlabel("Date")
plt.ylabel("Meals Consumed")
plt.title("Meals Consumed Over Time")
plt.show()