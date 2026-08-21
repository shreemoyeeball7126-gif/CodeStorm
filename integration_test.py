from predict import predict_demand
from surplus_logic import process_surplus, recipients


predicted_demand = predict_demand(
    day_of_week="Monday",
    weather="Sunny",
    attendance_pct=80
)

print("Predicted demand:", predicted_demand, "meals")

meals_prepared = 550

print("Meals prepared:", meals_prepared)


result = process_surplus(
    meals_prepared=meals_prepared,
    predicted_demand=predicted_demand,
    storage_time=1,
    temperature=4,
    recipients=recipients
)



print("\n--- FINAL RESULT ---")

print("Predicted demand:", predicted_demand)
print("Meals prepared:", meals_prepared)
print("Surplus:", result["surplus"])
print("Food safe:", result["safe"])
print("Redistributed:", result["redistributed"])
print("Unmatched:", result["unmatched"])

print("\nAllocations:")

for allocation in result["allocations"]:
    print(
        allocation["recipient"],
        "->",
        allocation["meals"],
        "meals"
    )