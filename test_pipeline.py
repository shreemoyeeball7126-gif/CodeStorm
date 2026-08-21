from impact import calculate_impact

from pipeline import (
    load_data,
    get_date_data,
    calculate_surplus,
    convert_to_kg,
    run_pipeline
)


print()
print(
    "================================"
)

print(
    "       FOODWISE TESTING"
)

print(
    "================================"
)

print()


# ==========================================
# TEST 1
# CHECK 250 DAYS
# ==========================================

df = load_data()


assert len(df) == 250


print(
    "✅ 250-day dataset test PASSED"
)


# ==========================================
# TEST 2
# FIRST DATE
# ==========================================

row = get_date_data(
    df,
    "2025-01-01"
)


assert row is not None


print(
    "✅ First date test PASSED"
)


# ==========================================
# TEST 3
# LAST DATE
# ==========================================

row = get_date_data(
    df,
    "2025-09-07"
)


assert row is not None


print(
    "✅ Last date test PASSED"
)


# ==========================================
# TEST 4
# SURPLUS
# ==========================================

surplus = calculate_surplus(
    1000,
    900
)


assert surplus == 100


print(
    "✅ Surplus calculation PASSED"
)


# ==========================================
# TEST 5
# NO NEGATIVE SURPLUS
# ==========================================

surplus = calculate_surplus(
    800,
    900
)


assert surplus == 0


print(
    "✅ Negative surplus protection PASSED"
)


# ==========================================
# TEST 6
# KG CONVERSION
# ==========================================

kg = convert_to_kg(
    100
)


assert kg == 10


print(
    "✅ KG conversion PASSED"
)


# ==========================================
# TEST 7
# IMPACT
# ==========================================

impact = calculate_impact(
    10
)


assert (
    impact["food_saved_kg"]
    == 10
)


assert (
    impact["money_saved"]
    == 1000
)


assert (
    impact["carbon_saved_kg"]
    == 21
)


print(
    "✅ Impact calculation PASSED"
)


# ==========================================
# TEST 8
# COMPLETE PIPELINE
# ==========================================

result = run_pipeline(
    "2025-01-01",
    storage_time=2,
    temperature=4
)


assert (
    "predicted_demand"
    in result
)


assert (
    "surplus_meals"
    in result
)


assert (
    "surplus_kg"
    in result
)


assert (
    "food_saved_kg"
    in result
)


assert (
    "money_saved"
    in result
)


assert (
    "carbon_saved_kg"
    in result
)


print(
    "✅ Complete pipeline PASSED"
)


# ==========================================
# TEST 9
# CHECK VALUES
# ==========================================

assert (
    result["surplus_meals"] >= 0
)


assert (
    result["surplus_kg"] >= 0
)


assert (
    result["food_saved_kg"] >= 0
)


assert (
    result["money_saved"] >= 0
)


assert (
    result["carbon_saved_kg"] >= 0
)


print(
    "✅ Output validation PASSED"
)


print()

print(
    "🎉 ALL TESTS PASSED!"
)

print(
    "Your complete pipeline is working."
)