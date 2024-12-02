def redistribute_male_numbers(original_5_14, original_15_24, original_25_49, original_50_plus):
    total_males = original_5_14 + original_15_24 + original_25_49 + original_50_plus

    # Redistribute to the new age groups
    male_5_9 = round(original_5_14 * 0.5)  # Assume half of 5-14 are 5-9
    male_10_19 = original_5_14 - male_5_9 + round(original_15_24 * 0.5)  # Rest of 5-14 and half of 15-24
    male_20_49 = original_25_49 + round(original_15_24 * 0.5)  # 25-49 and rest of 15-24
    male_50_plus_new = original_50_plus  # This remains the same

    # Adjust to ensure the total remains the same
    difference = total_males - (male_5_9 + male_10_19 + male_20_49 + male_50_plus_new)
    if difference != 0:
        male_20_49 += difference  # Add or subtract the difference from the largest group

    # Return a list of original and redistributed data
    return [
        ('5-14 years', original_5_14, male_5_9),
        ('15-24 years', original_15_24, male_10_19),
        ('25-49 years', original_25_49, male_20_49),
        ('50+ years', original_50_plus, male_50_plus_new),
    ]
