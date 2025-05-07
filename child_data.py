# Let's prepare the data and logic first in Python, then I'll provide the Flask app and HTML template accordingly.
# We'll start by defining the age rounding and vaccine schedule logic based on the user's specifications.

import math
from datetime import datetime

# Load child_data
child_data = {
    "male": {
        "Month 1": {"height": 56.5, "weight": 4.5},
        "Month 2": {"height": 60.0, "weight": 5.6},
        "Month 3": {"height": 63.5, "weight": 6.7},
        "Month 4": {"height": 66.0, "weight": 7.5},
        "Month 5": {"height": 68.0, "weight": 8.0},
        "Month 6": {"height": 70.0, "weight": 8.5},
        "Month 7": {"height": 71.5, "weight": 8.8},
        "Month 8": {"height": 73.0, "weight": 9.0},
        "Month 9": {"height": 74.5, "weight": 9.3},
        "Month 10": {"height": 75.5, "weight": 9.5},
        "Month 11": {"height": 76.5, "weight": 9.8},
        "Month 12": {"height": 77.5, "weight": 10.0},
    },
    "female": {
        "Month 1": {"height": 55.0, "weight": 4.2},
        "Month 2": {"height": 58.0, "weight": 5.2},
        "Month 3": {"height": 61.5, "weight": 6.1},
        "Month 4": {"height": 64.0, "weight": 6.8},
        "Month 5": {"height": 66.0, "weight": 7.3},
        "Month 6": {"height": 68.0, "weight": 7.8},
        "Month 7": {"height": 69.5, "weight": 8.1},
        "Month 8": {"height": 71.0, "weight": 8.4},
        "Month 9": {"height": 72.5, "weight": 8.7},
        "Month 10": {"height": 73.5, "weight": 8.9},
        "Month 11": {"height": 74.5, "weight": 9.2},
        "Month 12": {"height": 75.5, "weight": 9.4},
    }
}

# Sample vaccine milestones
vaccine_schedule = {
    1: ["BCG completed"],
    2: ["Penta-1 completed"],
    3: ["Penta-2 completed"],
    4: ["Penta-3 completed"],
    9: ["Measles completed"]
}

def parse_age(age_decimal):
    months = int(age_decimal)
    days_decimal = age_decimal - months
    days = int(days_decimal * 100)
    if days > 30:
        months += 1
        days = 1
    return months, days

def get_growth_data(gender, age_decimal, entered_height):
    months, days = parse_age(age_decimal)
    label = f"Month {months}"
    data = child_data.get(gender, {}).get(label)

    if not data:
        return None

    std_height = data["height"]
    if entered_height > std_height:
        verdict = "Above average"
    elif entered_height < std_height:
        verdict = "Below average"
    else:
        verdict = "Normal"

    vaccines = []
    for m, v in vaccine_schedule.items():
        if months >= m:
            vaccines.extend(v)

    return {
        "month_label": label,
        "standard_height": std_height,
        "entered_height": entered_height,
        "verdict": verdict,
        "vaccines": vaccines,
        "age_string": f"{months} months {days} days"
    }

