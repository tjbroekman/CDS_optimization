import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Parameters
homes = 55
intervals_per_day = 96  # 15-minute intervals
days_per_year = 366     # Leap year!
total_intervals = intervals_per_day * days_per_year

# Time index for leap year (2024 is a leap year)
start_time = datetime(2024, 1, 1)
timestamps = [start_time + timedelta(minutes=15 * i) for i in range(total_intervals)]

# Function to generate a realistic load profile for one home
def generate_single_home_profile():
    profile = []
    for day in range(days_per_year):
        daily_profile = []
        for i in range(intervals_per_day):
            hour = (i * 15) / 60
            # Simulated load pattern (no heating)
            if 0 <= hour < 6:
                base = np.random.uniform(0.1, 0.3)
            elif 6 <= hour < 9:
                base = np.random.uniform(0.5, 1.5)
            elif 9 <= hour < 17:
                base = np.random.uniform(0.3, 0.8)
            elif 17 <= hour < 22:
                base = np.random.uniform(1.0, 2.5)
            else:
                base = np.random.uniform(0.3, 1.0)
            noise = np.random.normal(0, 0.05)
            daily_profile.append(max(base + noise, 0))  # No negative values
        profile.extend(daily_profile)
    return profile

# Generate profiles for each home
data = {f'Home_{i+1}': generate_single_home_profile() for i in range(homes)}

# Create DataFrame
df = pd.DataFrame(data, index=pd.to_datetime(timestamps))
df.index.name = "Timestamp"

# Add total load column
df["Total_Load_kW"] = df.sum(axis=1)

# Save full dataset
df.to_csv("residential_load_profiles_55_homes_leap_year.csv", sep=";")

# Save just the total community load
df[["Total_Load_kW"]].to_csv("total_community_load_55_homes_leap_year.csv", sep=";")

print("✅ Files saved:\n - residential_load_profiles_55_homes_leap_year.csv\n - total_community_load_55_homes_leap_year.csv")
