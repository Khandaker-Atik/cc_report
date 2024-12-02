import random
from datetime import datetime, timedelta

# Expanded male names and upadhi
male_names = [
    "Aaraf", "Aariz", "Abrar", "Adnan", "Afif", "Ahsan", "Alam", "Anis", "Arham", "Ashfaq",
    "Aslam", "Azad", "Bashir", "Bilal", "Emon", "Farid", "Galib", "Habib", "Iqbal", "Irfan",
    "Jahid", "Jamal", "Kaiser", "Karim", "Latif", "Mahfuz", "Mansur", "Masud", "Mustafa", "Nabil",
    "Nasim", "Nazim", "Omar", "Pavel", "Qadir", "Rafiq", "Rakib", "Sajid", "Shahid", "Tanvir",
    "Tariq", "Tasnim", "Umar", "Usman", "Wahid", "Yasir", "Zafar", "Zakir", "Zia", "Zubair"
]

male_upadhi = [
    "Bhuiyan", "Chowdhury", "Das", "Gazi", "Haque", "Hossain", "Islam", "Khan", "Majumder", "Mia",
    "Mondal", "Morshed", "Munshi", "Noor", "Patwary", "Quader", "Rahman", "Sarker", "Sheikh", "Uddin",
    "Yusuf", "Zaman"
]

# Expanded female names and upadhi
female_names = [
    "Afreen", "Amina", "Bristi", "Dalia", "Elma", "Farzana", "Gulshan", "Habiba", "Ishrat", "Jasmin",
    "Kaniz", "Lamia", "Mahiya", "Nadia", "Nahida", "Oishee", "Parveen", "Rahima", "Sabiha", "Samina",
    "Shabana", "Sharmin", "Tabassum", "Tamanna", "Umme", "Yasmin", "Zarina"
]

female_upadhi = [
    "Akter", "Begum", "Chowdhury", "Khatun", "Majumder", "Mondal", "Nasrin", "Rahman", "Sarker", "Sultana"
]

def generate_birthdate(gender):
    """Generates a random birthdate based on gender."""
    today = datetime.today()
    start_date = today - timedelta(days=31*365)  # 31 years ago
    end_date = today - timedelta(days=18*365)    # 18 years ago
    return datetime.fromtimestamp(random.randint(int(start_date.timestamp()), int(end_date.timestamp())))

def calculate_age(birthdate):
    """Calculates age from the given birthdate."""
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def age_in_words(age, birthdate):
    years = age
    months = (datetime.today().month - birthdate.month) % 12
    days = (datetime.today() - birthdate.replace(year=birthdate.year + age)).days
    return f"Age: {years} years, {months} months, {days} days"

def generate_weight_and_height(age, gender):
    """Generates random weight and height based on age and gender."""
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
    else:  # Male ranges (you can adjust based on your needs)
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
    """Generates a random LMP date between 4 to 6 months ago."""
    today = datetime.today()
    # LMP date between 4 months (120 days) and 6.5 months (195 days) ago
    start_lmp = today - timedelta(days=195)  # 6.5 months ago
    end_lmp = today - timedelta(days=120)   # 4 months ago
    lmp_date = datetime.fromtimestamp(random.randint(int(start_lmp.timestamp()), int(end_lmp.timestamp())))
    return lmp_date.strftime('%Y-%m-%d')  # Format the LMP date as yyyy-mm-dd
if __name__ == "__main__":
    gender = input("Enter 'm' for male or 'f' for female: ").lower()

    if gender == 'm':
        print("User Input: MALE\n")
        generated_name = random.choice(male_names) + " " + random.choice(male_upadhi)
        fathers_name = random.choice(male_names) + " " + random.choice(male_upadhi)
        mothers_name = random.choice(female_names) + " " + random.choice(female_upadhi)
        birthdate = generate_birthdate()
        age = calculate_age(birthdate)
        age_str = age_in_words(age, birthdate)
        weight, height = generate_weight_and_height(age, gender)
        print()
        print("......................................")
        print()
        print("Name:", generated_name)
        print("Fathers Name:", fathers_name)
        print("Mothers Name:", mothers_name)
        print("Birthdate:", birthdate.strftime("%Y-%m-%d"))
        print(age_str)
        print("Weight:", weight, "kg")
        print("Height:", height, "cm")
        print()
        print("......................................")
        print()
    elif gender == 'f':
        print("User Input: FEMALE\n")
        generated_name = random.choice(female_names) + " " + random.choice(female_upadhi)
        fathers_name = random.choice(male_names) + " " + random.choice(male_upadhi)
        mothers_name = random.choice(female_names) + " " + random.choice(female_upadhi)
        birthdate = generate_birthdate()
        age = calculate_age(birthdate)
        age_str = age_in_words(age, birthdate)
        weight, height = generate_weight_and_height(age, gender)
        lmp_date = generate_lmp_date()  # Generate LMP date
        print()
        print("......................................")
        print()
        print("Name:", generated_name)
        print("Fathers Name:", fathers_name)
        print("Mothers Name:", mothers_name)
        print("Birthdate:", birthdate.strftime("%Y-%m-%d"))
        print(age_str)
        print("Weight:", weight, "kg")
        print("Height:", height, "cm")
        print("LMP Date:", lmp_date)
        print()
        print("......................................")
        print()
    else:
        print("Invalid input. Please enter 'm' for male or 'f' for female.")
