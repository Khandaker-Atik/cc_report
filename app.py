from flask import Flask, render_template, request, session
import random
from datetime import datetime, timedelta
import requests
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# --------------------------------------------
# Google Sheets Integration
# --------------------------------------------

# Your Google Sheet ID (extracted from the URL)
SHEET_ID = '1w2zBjdLpfwVwde_FCy17ACIOq8JJDlxMlcZGN1JgEpU'
SHEET_NAME = 'Sheet1'  # Change this if your sheet has a different name

def fetch_names_from_google_sheets():
    """Fetch names from Google Sheets and organize by gender"""
    try:
        # Construct the CSV export URL
        csv_url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
        
        # Fetch the CSV data
        response = requests.get(csv_url)
        response.raise_for_status()
        
        # Parse CSV data
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        
        male_names = []
        female_names = []
        
        for row in reader:
            name = row.get('Name', '').strip()
            gender = row.get('Gender', '').strip()
            
            if name:  # Only add non-empty names
                if gender == '0':  # Male
                    male_names.append(name)
                elif gender == '1':  # Female
                    female_names.append(name)
        
        return male_names, female_names
    
    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")
        # Return fallback names if Google Sheets fails
        return get_fallback_names()

def get_fallback_names():
    """Fallback names in case Google Sheets is unavailable"""
    male_names = [
        "সবুজ হোসাইন", "গানেম", "জালাল", "আকবার", "রহিম", "করিম", "আলম", "সালাম"
    ]
    female_names = [
        "চঞ্চলা", "রহিমা", "সালমা", "ফাতেমা", "আয়েশা", "খাদিজা"
    ]
    return male_names, female_names

# Fetch names at startup
try:
    MALE_NAMES_FROM_SHEETS, FEMALE_NAMES_FROM_SHEETS = fetch_names_from_google_sheets()
except:
    MALE_NAMES_FROM_SHEETS, FEMALE_NAMES_FROM_SHEETS = get_fallback_names()

# --------------------------------------------
# Original Name Generator Data & Functions
# --------------------------------------------


def get_random_name(gender, use_sheets_data=True):
    """Get a random name based on gender"""
    if use_sheets_data and len(MALE_NAMES_FROM_SHEETS) > 0 and len(FEMALE_NAMES_FROM_SHEETS) > 0:
        if gender == 'm':
            return random.choice(MALE_NAMES_FROM_SHEETS)
        else:
            return random.choice(FEMALE_NAMES_FROM_SHEETS)
    else:
        # Use original name generation logic
        if gender == 'm':
            return random.choice(male_names) + " " + random.choice(male_upadhi)
        else:
            return random.choice(female_names) + " " + random.choice(female_upadhi)

def generate_birthdate(gender):
    today = datetime.today()
    start_date = today - timedelta(days=31*365)
    end_date = today - timedelta(days=18*365)
    return datetime.fromtimestamp(random.randint(int(start_date.timestamp()), int(end_date.timestamp())))

def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def generate_weight_and_height(age, gender):
    if gender == 'f':
        if 18 <= age <= 24:
            weight = round(random.uniform(45, 55), 2)
            height = round(random.uniform(150, 160), 2)
        elif 25 <= age <= 30:
            weight = round(random.uniform(50, 60), 2)
            height = round(random.uniform(150, 160), 2)
        elif 31 <= age <= 40:
            weight = round(random.uniform(55, 65), 2)
            height = round(random.uniform(150, 160), 2)
        else:
            weight = round(random.uniform(55, 65), 2)
            height = round(random.uniform(150, 160), 2)
    else:
        if 18 <= age <= 24:
            weight = round(random.uniform(55, 65), 2)
            height = round(random.uniform(160, 175), 2)
        elif 25 <= age <= 30:
            weight = round(random.uniform(60, 75), 2)
            height = round(random.uniform(165, 175), 2)
        elif 31 <= age <= 40:
            weight = round(random.uniform(65, 80), 2)
            height = round(random.uniform(165, 175), 2)
        else:
            weight = round(random.uniform(65, 80), 2)
            height = round(random.uniform(165, 175), 2)
    return weight, height

def generate_lmp_date():
    today = datetime.today()
    start_lmp = today - timedelta(days=195)  # 6.5 months ago
    end_lmp = today - timedelta(days=120)    # 4 months ago
    lmp_date = datetime.fromtimestamp(random.randint(int(start_lmp.timestamp()), int(end_lmp.timestamp())))
    return lmp_date.strftime('%Y-%m-%d')

# --------------------------------------------
# Population Distribution
# --------------------------------------------

def distribute_numbers(total_population):
    age_groups = [0.2, 0.3, 0.4, 0.1]  # 20%, 30%, 40%, 10%
    distributed = [int(total_population * p) for p in age_groups]
    
    # Calculate the difference due to rounding and add it to the largest group
    difference = total_population - sum(distributed)
    if difference != 0:
        # Add the difference to the largest age group (25-49 years, index 2)
        distributed[2] += difference
    
    return distributed

# --------------------------------------------
# Age Redistribution (for male)
# --------------------------------------------

def redistribute_male_numbers(original_5_14, original_15_24, original_25_49, original_50_plus):
    total_males = original_5_14 + original_15_24 + original_25_49 + original_50_plus

    male_5_9 = round(original_5_14 * 0.5)
    male_10_19 = original_5_14 - male_5_9 + round(original_15_24 * 0.5)
    male_20_49 = original_25_49 + round(original_15_24 * 0.5)
    male_50_plus_new = original_50_plus

    difference = total_males - (male_5_9 + male_10_19 + male_20_49 + male_50_plus_new)
    if difference != 0:
        male_20_49 += difference

    return [
        ('5-14 years', original_5_14, male_5_9),
        ('15-24 years', original_15_24, male_10_19),
        ('25-49 years', original_25_49, male_20_49),
        ('50+ years', original_50_plus, male_50_plus_new),
    ]

# --------------------------------------------
# Child Growth Data and Helpers
# --------------------------------------------

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

def get_growth_data(gender, age_decimal):
    months, days = parse_age(age_decimal)
    label = f"Month {months}"
    data = child_data.get(gender, {}).get(label)
    if not data:
        return None

    std_height = data["height"]
    std_weight = data["weight"]

    vaccines = []
    for m, v in vaccine_schedule.items():
        if months >= m:
            vaccines.extend(v)

    return {
        "month_label": label,
        "standard_height": std_height,
        "standard_weight": std_weight,
        "vaccines": vaccines,
        "age_string": f"{months} months {days} days"
    }

# --------------------------------------------
# Flask Routes
# --------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/population-distribution', methods=['GET', 'POST'])
def population_distribution():
    if request.method == 'POST':
        total_male = int(request.form['total_male'])
        total_female = int(request.form['total_female'])

        male_numbers = distribute_numbers(total_male)
        female_numbers = distribute_numbers(total_female)

        return render_template('population_distribution.html', 
                               male_numbers=male_numbers, 
                               female_numbers=female_numbers, 
                               total_male=total_male, 
                               total_female=total_female)

    # For GET requests, pass None values to avoid template errors
    return render_template('population_distribution.html', 
                           male_numbers=None, 
                           female_numbers=None, 
                           total_male=None, 
                           total_female=None)

@app.route('/name-generator', methods=['GET', 'POST'])
def name_generator():
    if request.method == 'POST':
        gender = request.form.get('gender', '').lower()
        session['gender'] = gender  # Store selected gender in session
        
        # Option to refresh names from Google Sheets
        refresh_names = request.form.get('refresh_names', False)
        if refresh_names:
            global MALE_NAMES_FROM_SHEETS, FEMALE_NAMES_FROM_SHEETS
            try:
                MALE_NAMES_FROM_SHEETS, FEMALE_NAMES_FROM_SHEETS = fetch_names_from_google_sheets()
            except:
                pass  # Continue with existing names if refresh fails
    else:
        gender = session.get('gender', None)

    if gender in ['m', 'f']:
        # Use names from Google Sheets
        generated_name = get_random_name(gender, use_sheets_data=True)
        fathers_name = get_random_name('m', use_sheets_data=True)
        mothers_name = get_random_name('f', use_sheets_data=True)
        
        if gender == 'f':
            lmp_date = generate_lmp_date()
        else:
            lmp_date = None

        birthdate = generate_birthdate(gender)
        age = calculate_age(birthdate)
        weight, height = generate_weight_and_height(age, gender)

        # Pass sheet info to template
        sheet_info = {
            'male_count': len(MALE_NAMES_FROM_SHEETS),
            'female_count': len(FEMALE_NAMES_FROM_SHEETS),
            'using_sheets': len(MALE_NAMES_FROM_SHEETS) > 0 and len(FEMALE_NAMES_FROM_SHEETS) > 0
        }

        return render_template('name_generator.html', 
                               generated_name=generated_name, 
                               fathers_name=fathers_name, 
                               mothers_name=mothers_name, 
                               birthdate=birthdate.strftime("%Y-%m-%d"), 
                               age=age, 
                               weight=weight, 
                               height=height,
                               gender=gender,
                               lmp_date=lmp_date,
                               sheet_info=sheet_info)

    # No gender selected yet (GET first time)
    sheet_info = {
        'male_count': len(MALE_NAMES_FROM_SHEETS),
        'female_count': len(FEMALE_NAMES_FROM_SHEETS),
        'using_sheets': len(MALE_NAMES_FROM_SHEETS) > 0 and len(FEMALE_NAMES_FROM_SHEETS) > 0
    }
    return render_template('name_generator.html', sheet_info=sheet_info)

@app.route('/child-data', methods=['GET', 'POST'])
def child_growth_data():
    result = None
    error_message = None

    if request.method == 'POST':
        gender = request.form.get('gender')
        age_input = request.form.get('age')

        try:
            age_input = float(age_input)
            result = get_growth_data(gender, age_input)
            if not result:
                error_message = "No data found for this age."
        except (ValueError, TypeError):
            error_message = "Invalid age input. Please enter a valid number."

    male_heights = [data['height'] for data in child_data['male'].values()]
    female_heights = [data['height'] for data in child_data['female'].values()]
    male_weights = [data['weight'] for data in child_data['male'].values()]
    female_weights = [data['weight'] for data in child_data['female'].values()]
    labels = list(child_data['male'].keys())

    return render_template(
        'child_data.html', 
        child_data=child_data,
        male_heights=male_heights,
        female_heights=female_heights,
        male_weights=male_weights,
        female_weights=female_weights,
        labels=labels,
        result=result,
        error_message=error_message
    )

@app.route('/age-redistribution', methods=['GET', 'POST'])
def age_redistribution():
    redistributed_data = None
    original_data = {}

    if request.method == 'POST':
        original_5_14 = int(request.form['original_5_14'])
        original_15_24 = int(request.form['original_15_24'])
        original_25_49 = int(request.form['original_25_49'])
        original_50_plus = int(request.form['original_50_plus'])

        original_data = {
            '5-14': original_5_14,
            '15-24': original_15_24,
            '25-49': original_25_49,
            '50+': original_50_plus
        }

        redistributed_data = redistribute_male_numbers(original_5_14, original_15_24, original_25_49, original_50_plus)

    return render_template('age_redistribution.html', redistributed_data=redistributed_data, original_data=original_data)

@app.route('/refresh-names')
def refresh_names():
    """Endpoint to manually refresh names from Google Sheets"""
    global MALE_NAMES_FROM_SHEETS, FEMALE_NAMES_FROM_SHEETS
    try:
        MALE_NAMES_FROM_SHEETS, FEMALE_NAMES_FROM_SHEETS = fetch_names_from_google_sheets()
        return {"status": "success", "male_count": len(MALE_NAMES_FROM_SHEETS), "female_count": len(FEMALE_NAMES_FROM_SHEETS)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    app.run(debug=True)