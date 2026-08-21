# impact.py


AVERAGE_COST_PER_KG = 100

CARBON_FACTOR = 2.1


def calculate_impact(surplus_kg):

    surplus_kg = float(surplus_kg)

    if surplus_kg < 0:
        surplus_kg = 0

    food_saved_kg = surplus_kg

    money_saved = (
        surplus_kg * AVERAGE_COST_PER_KG
    )

    carbon_saved_kg = (
        surplus_kg * CARBON_FACTOR
    )

    return {
        "food_saved_kg": round(
            food_saved_kg,
            2
        ),

        "money_saved": round(
            money_saved,
            2
        ),

        "carbon_saved_kg": round(
            carbon_saved_kg,
            2
        )
    }


# Test the function
if __name__ == "__main__":

    result = calculate_impact(10)

    print("Food saved:", result["food_saved_kg"], "kg")

    print("Money saved: ₹", result["money_saved"])

    print(
        "Carbon avoided:",
        result["carbon_saved_kg"],
        "kg CO2e"
    )