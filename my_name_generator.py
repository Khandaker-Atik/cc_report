from datetime import datetime
import random

# Bangladeshi Male Names (no Upadhi in the names)
male_names = [
    "Abdul", "Ali", "Amin", "Anwar", "Arif", "Asad", "Ashraf", "Babul", "Bashir", "Daud", 
    "Faisal", "Farid", "Golam", "Habib", "Harun", "Ibrahim", "Imran", "Jamal", "Kamal", "Kabir", 
    "Liton", "Mamun", "Masud", "Mizan", "Moin", "Monir", "Mosharraf", "Mujibur", "Mukul", "Munir", 
    "Nasir", "Nur", "Osman", "Rafiq", "Rahim", "Rahman", "Riaz", "Rony", "Sadek", "Sajjad", 
    "Salim", "Sayed", "Shahid", "Shahin", "Shahjahan", "Shakil", "Tarek", "Zakir", "Zia"
]

# Bangladeshi Female Names (no Upadhi in the names)
female_names = [
    "Afsana", "Afsari", "Afroza", "Aleya", "Anjuman", "Arifa", "Arzoo", "Asha", "Asma", "Badrun", 
    "Champa", "Farzana", "Firoza", "Halima", "Hasina", "Jahan", "Jahanara", "Jasmin", "Khaleda", 
    "Khurshida", "Lipi", "Mala", "Mina", "Nadia", "Nahida", "Nasima", "Nila", "Nusrat", "Papia", 
    "Parvin", "Rabeya", "Rina", "Rokhsana", "Rokeya", "Rubina", "Runa", "Sabina", "Sadia", "Sakina", 
    "Sultana", "Sumi", "Tahmina", "Tania", "Taslima", "Yasmin", "Zahida", "Zahura","Rubi"
]

# Upadhi (surnames)
male_upadhi = ["Mia", "Khan", "Ahmed", "Rashid", "Chowdhury", "Talukder", "Hossain", "Molla", "Sarkar", "Joardar", "Khandaker"]
female_upadhi = ["Begum", "Khatun", "Sultana", "Akter", "Rani", "Bibi", "Nabi"]

def generate_birthdate(gender):
    """Generates a random birthdate based on gender."""
    if gender == 'm':
        start_date = datetime(1960, 1, 1)  # Male birthdate range
        end_date = datetime(2005, 12, 31)
    else:
        start_date = datetime(1990, 1, 1)  # Female birthdate range
        end_date = datetime(2005, 12, 31)
    
    return start_date + (end_date - start_date) * random.random()

def calculate_age(birthdate):
    """Calculates age from the given birthdate."""
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def generate_weight_and_height(age, gender):
    """Generates random weight and height based on age and gender."""
    if gender == 'm':
        weight = random.randint(50, 85)  # Male weight in kg (Bangladeshi average)
        height = random.randint(160, 183)  # Male height in cm
    else:
        weight = random.randint(42, 60)  # Female weight in kg (Bangladeshi average)
        height = random.randint(150, 170)  # Female height in cm
    return weight, height

def generate_name(gender):
    """Generates a random name with Upadhi (surname). Only the first name is returned."""
    if gender == 'm':
        first_name = random.choice(male_names)
        # Returning only the first name, no Upadhi
        return first_name
    else:
        first_name = random.choice(female_names)
        # Returning only the first name, no Upadhi
        return first_name

# Example usage:
# For Male
male_name = generate_name('m')  # Pass 'm' for male
male_birthdate = generate_birthdate('m')  # Pass 'm' for male
male_age = calculate_age(male_birthdate)
male_weight, male_height = generate_weight_and_height(male_age, 'm')

print(f"Male Name: {male_name}")
print(f"Male Birthdate: {male_birthdate}")
print(f"Male Age: {male_age}")
print(f"Male Weight: {male_weight} kg")
print(f"Male Height: {male_height} cm")

# For Female
female_name = generate_name('f')  # Pass 'f' for female
female_birthdate = generate_birthdate('f')  # Pass 'f' for female
female_age = calculate_age(female_birthdate)
female_weight, female_height = generate_weight_and_height(female_age, 'f')

print(f"Female Name: {female_name}")
print(f"Female Birthdate: {female_birthdate}")
print(f"Female Age: {female_age}")
print(f"Female Weight: {female_weight} kg")
print(f"Female Height: {female_height} cm")

