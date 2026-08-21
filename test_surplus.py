from surplus_logic import process_surplus, recipients

result = process_surplus(
    meals_prepared=550,
    predicted_demand=496,
    storage_time=2,
    temperature=4,
    recipients=recipients
)

print("\n--- SURPLUS TEST ---")
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