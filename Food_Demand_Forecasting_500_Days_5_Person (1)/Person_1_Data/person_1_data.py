# PERSON 1 — Generate and validate 500 days of data.

from datetime import date, timedelta
import numpy as np
import pandas as pd

SEED = 42
DAYS = 500
END_DATE = date(2026, 8, 21)
START_DATE = END_DATE - timedelta(days=DAYS - 1)

# Generate the same dataset structure as demand_data.csv.
# Attendance is always between 0 and 100.

# See demand_data.csv for the generated 500-day dataset.
