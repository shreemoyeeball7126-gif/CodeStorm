# Food Demand Forecasting — 5 Person Project

This version contains **500 days of data**.

- Start date: 2025-04-09
- End date: 2026-08-21
- Total rows: 500
- Attendance is always 0–100%.
- Preparation buffer: 3.8%.
- Example: 438 predicted → 455 recommended → 17 surplus.
- Surplus is assigned to verified demo donation recipients.

## Run

pip install -r requirements.txt

streamlit run Person_4_Dashboard/app.py

For integration testing:

python Person_5_Impact_Integration/person_5_integration_test.py
