# PERSON 3 — Minimal surplus and donation recommendation.

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPIENT_FILE = ROOT / "Person_3_Surplus_Donation" / "recipients.csv"

# Small preparation buffer.
# 438 predicted -> 455 recommended -> 17 surplus.
PREPARATION_BUFFER = 0.038

def recommended_preparation(predicted_demand):
    predicted_demand = max(0, float(predicted_demand))
    return max(
        int(round(predicted_demand)),
        int(round(predicted_demand * (1 + PREPARATION_BUFFER)))
    )

def calculate_surplus(recommended, predicted):
    return max(0, int(recommended) - int(round(predicted)))

def donation_recommendation(surplus):
    surplus = max(0, int(surplus))
    if surplus == 0:
        return []

    recipients = pd.read_csv(RECIPIENT_FILE)
    eligible = recipients[recipients["verified"].astype(bool)].copy()
    eligible = eligible.sort_values(
        ["priority", "distance_km"],
        ascending=[False, True]
    )

    remaining = surplus
    allocations = []

    for _, row in eligible.iterrows():
        if remaining <= 0:
            break

        qty = min(remaining, int(row["capacity_meals"]))

        if qty > 0:
            allocations.append({
                "recipient": row["recipient_name"],
                "type": row["recipient_type"],
                "recommended_meals": qty,
                "capacity": int(row["capacity_meals"]),
                "distance_km": float(row["distance_km"]),
                "priority": int(row["priority"])
            })
            remaining -= qty

    return allocations

if __name__ == "__main__":
    predicted = 438
    recommended = recommended_preparation(predicted)
    surplus = calculate_surplus(recommended, predicted)
    print("Predicted:", predicted)
    print("Recommended:", recommended)
    print("Surplus:", surplus)
    print(pd.DataFrame(donation_recommendation(surplus)))
