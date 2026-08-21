recipients = [
    {
        "name": "NGO A",
        "capacity": 40,
        "distance_km": 3,
        "priority": 1
    },
    {
        "name": "Shelter B",
        "capacity": 30,
        "distance_km": 5,
        "priority": 2
    },
    {
        "name": "Hostel C",
        "capacity": 50,
        "distance_km": 2,
        "priority": 3
    }
]


def calculate_surplus(meals_prepared, predicted_demand):
    """
    Calculate the number of surplus meals.

    If prepared food is less than or equal to predicted demand,
    surplus is 0.
    """

    surplus = meals_prepared - predicted_demand

    return max(0, surplus)


def check_food_safety(storage_time, temperature):
    """
    Check whether food is eligible for redistribution.

    NOTE:
    These are temporary prototype values.
    They must be replaced/verified using appropriate
    food-safety guidance before the final submission.
    """

    MAX_STORAGE_TIME = 2
    MIN_TEMP = 0
    MAX_TEMP = 5

    if storage_time > MAX_STORAGE_TIME:
        return False

    if temperature < MIN_TEMP or temperature > MAX_TEMP:
        return False

    return True


def match_surplus(surplus, recipients):
    """
    Allocate surplus meals among eligible recipients.

    Recipients are sorted by:
    1. Priority (higher priority first)
    2. Distance (closer first if priority is the same)
    """

    # Sort recipients
    sorted_recipients = sorted(
        recipients,
        key=lambda x: (x["priority"], x["distance_km"])
    )

    allocations = []
    remaining = surplus

    for recipient in sorted_recipients:

        # Stop if there is no surplus left
        if remaining <= 0:
            break

        # Cannot give more than recipient's capacity
        amount = min(
            remaining,
            recipient["capacity"]
        )

        allocations.append({
            "recipient": recipient["name"],
            "meals": amount
        })

        remaining -= amount

    return allocations, remaining


def process_surplus(
    meals_prepared,
    predicted_demand,
    storage_time,
    temperature,
    recipients
):
    """
    Complete surplus-management pipeline:

    1. Calculate surplus
    2. Check food safety
    3. Match safe surplus to recipients
    4. Return complete results
    """

    # Step 1: Calculate surplus
    surplus = calculate_surplus(
        meals_prepared,
        predicted_demand
    )

    # Case 1: No surplus
    if surplus == 0:
        return {
            "surplus": 0,
            "safe": None,
            "allocations": [],
            "redistributed": 0,
            "unmatched": 0
        }

    # Step 2: Check safety
    safe = check_food_safety(
        storage_time,
        temperature
    )

    # Case 2: Surplus exists but food is unsafe
    if not safe:
        return {
            "surplus": surplus,
            "safe": False,
            "allocations": [],
            "redistributed": 0,
            "unmatched": surplus
        }

    # Step 3: Match safe surplus
    allocations, unmatched = match_surplus(
        surplus,
        recipients
    )

    # Step 4: Calculate successfully redistributed meals
    redistributed = surplus - unmatched

    return {
        "surplus": surplus,
        "safe": True,
        "allocations": allocations,
        "redistributed": redistributed,
        "unmatched": unmatched
    }

