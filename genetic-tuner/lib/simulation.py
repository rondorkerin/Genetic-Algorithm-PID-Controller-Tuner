def generate_initial_population():
    """
    1 [Start] Generate random population of n chromosomes (suitable solutions for the problem)
    Creates a random genome
    """
    random.seed()
    population = []
    for chromosome in range(POPULATION_SIZE):
        # create a random chromosome with a random gain value
        population.append(Chromosome(random.random() * MAX_GAIN_VALUE, random.random() * MAX_GAIN_VALUE, random.random() * MAX_GAIN_VALUE))
    return population

"""
2 [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
returns the fitness value according to the fitness function

takes in a list of distances, finds the sum of their squares and returns the inverse of it.
"""
def fitness(distance_list):
    sum = 0
    for i in range(len(distance_list)):
        sum = sum + distance_list[i]**2
    return 1 /  math.sqrt(sum)

