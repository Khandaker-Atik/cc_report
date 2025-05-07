from flask import Flask, render_template, request
from age_redis import redistribute_male_numbers
import random
from datetime import datetime
from population_distribution import distribute_numbers
from my_name_generator import (
    male_names, male_upadhi, 
    female_names, female_upadhi, 
    generate_birthdate, calculate_age, 
    generate_weight_and_height, generate_lmp_date
)
from child_data import child_data

app = Flask(__name__)

# Helper functions for child growth data
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

    vaccines = []
    vaccine_schedule = {
        1: ["BCG completed"],
        2: ["Penta-1 completed"],
        3: ["Penta-2 completed"],
        4: ["Penta-3 completed"],
        9: ["Measles completed"]
    }
    for m, v in vaccine_schedule.items():
        if months >= m:
            vaccines.extend(v)

    return {
        "month_label": label,
        "standard_height": std_height,
        "vaccines": vaccines,
        "age_string": f"{months} months {days} days"
    }

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

    return render_template('population_distribution.html')

@app.route('/name-generator', methods=['GET', 'POST'])
def name_generator():
    if request.method == 'POST':
        gender = request.form.get('gender', '').lower()

        if gender == 'm':
            generated_name = random.choice(male_names) + " " + random.choice(male_upadhi)
            fathers_name = random.choice(male_names) + " " + random.choice(male_upadhi)
            mothers_name = random.choice(female_names) + " " + random.choice(female_upadhi)
            lmp_date = None
        elif gender == 'f':
            generated_name = random.choice(female_names) + " " + random.choice(female_upadhi)
            fathers_name = random.choice(male_names) + " " + random.choice(male_upadhi)
            mothers_name = random.choice(female_names) + " " + random.choice(female_upadhi)
            lmp_date = generate_lmp_date()
        else:
            return "Invalid gender", 400

        birthdate = generate_birthdate(gender)
        age = calculate_age(birthdate)
        weight, height = generate_weight_and_height(age, gender)

        return render_template('name_generator.html', 
                               generated_name=generated_name, 
                               fathers_name=fathers_name, 
                               mothers_name=mothers_name, 
                               birthdate=birthdate.strftime("%Y-%m-%d"), 
                               age=age, 
                               weight=weight, 
                               height=height,
                               gender=gender,
                               lmp_date=lmp_date)

    return render_template('name_generator.html')

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

if __name__ == '__main__':
    app.run(debug=True)
