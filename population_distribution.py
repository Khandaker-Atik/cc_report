# population_distribution.py

def distribute_numbers(total_population):
    """
    Distributes the total population into predefined age groups
    based on proportional distribution.

    Arguments:
    total_population -- Total population to distribute across age groups.

    Returns:
    A list of populations for each age group (5-14, 15-24, 25-49, 50+).
    """
    # Example distribution percentages (adjust as needed)
    age_groups = [0.2, 0.3, 0.4, 0.1]  # 20% in 5-14, 30% in 15-24, 40% in 25-49, 10% in 50+
    
    # Calculate population for each group
    return [int(total_population * percentage) for percentage in age_groups]
