from flask import Flask, render_template, request
import random
from datetime import datetime
from population_distribution import distribute_numbers
from my_name_generator import (
    male_names, male_upadhi, 
    female_names, female_upadhi, 
    generate_birthdate, calculate_age, 
    generate_weight_and_height
)
from child_data import child_data

app = Flask(__name__)


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
        elif gender == 'f':
            generated_name = random.choice(female_names) + " " + random.choice(female_upadhi)
            fathers_name = random.choice(male_names) + " " + random.choice(male_upadhi)
            mothers_name = random.choice(female_names) + " " + random.choice(female_upadhi)
        else:
            return "Invalid gender", 400
        
        birthdate = generate_birthdate(gender)  # Pass gender to the function

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
                               gender=gender)
    
    return render_template('name_generator.html')

@app.route('/child-data')
def child_growth_data():
    male_heights = [data['height'] for data in child_data['male'].values()]
    female_heights = [data['height'] for data in child_data['female'].values()]
    male_weights = [data['weight'] for data in child_data['male'].values()]
    female_weights = [data['weight'] for data in child_data['female'].values()]
    labels = list(child_data['male'].keys())  # Convert keys to a list

    return render_template(
        'child_data.html', 
        child_data=child_data,
        male_heights=male_heights,
        female_heights=female_heights,
        male_weights=male_weights,
        female_weights=female_weights,
        labels=labels  # Pass labels to the template
    )


@app.route('/age-redistribution', methods=['GET', 'POST'])
def age_redistribution():
    if request.method == 'POST':
        # Placeholder for age redistribution logic
        pass
    return render_template('age_redistribution.html')

if __name__ == '__main__':
    app.run(debug=True)
