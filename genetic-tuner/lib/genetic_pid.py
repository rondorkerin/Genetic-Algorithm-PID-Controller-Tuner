import random
import math
from chromosome import Chromosome
import listtools
# TODO: Turn this into a class.

POPULATION_SIZE = 100
MUTATION_PROBABILITY = .1
CROSSOVER_RATE = .9
MAX_RUNS = 100

# Simulation Parameters
MAX_TIMESTEPS = 150
LINE_SMOOTHNESS = .1
MAX_GAIN_VALUE = 3


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

"""
Run simulation for a specific chromosome c.

Returns the fitness function value of the simulation
"""
def run_simulation_for_chromosome(map, population, chromosome):

    distance_list = []
    current_position = 0
    last_distance = 0
    current_summation = 0
    current_distance = 0

    for time in range(MAX_TIMESTEPS):
        current_distance = map[time] - current_position

        #for integral controller
        current_summation = current_summation + current_distance

        #x = x + dx/dt * dt (dt = 1)
        new_velocity = population[chromosome].kp * current_distance + population[chromosome].kd * (current_distance-last_distance) + population[chromosome].ki * current_distance
        current_position = current_position + new_velocity

        distance_list.append(current_distance)

        # for the derivative
        last_distance = current_distance

    return fitness(distance_list)

"""
Run the simulation for the set of all chromosomes
"""
def run_simulation(map, population):
    fitness_values = []
    for chromosome in range(POPULATION_SIZE):
        fitness_values.append(chromosome)
        fitness_values[chromosome] = run_simulation_for_chromosome(map, population, chromosome)

    return fitness_values

"""
Pick two parents according to probability represented by normalized fitness values
3a[Selection] Select two parent chromosomes from a population according to their fitness
Better fitness values increase the chance of being selected.
"""
def selection(fitness_values):
    # normalize the list so we have probabilities to pick parents
    fitness_values = listtools.normListSumTo(fitness_values, 1)
    # a list of parent indices.
    parents = []
    random.seed()
    parent1_probability = random.random()
    parent2_probability = random.random()

    sum = 0
    for i in range(POPULATION_SIZE):
        if len(parents) == 2:
            break
        next_sum = sum + fitness_values[i]
        if parent1_probability <= next_sum and parent1_probability >= sum:
            parents.append(i)
        if parent2_probability <= next_sum and parent2_probability >= sum:
            parents.append(i)
        sum = next_sum
    return parents

"""
3b[Crossover] With a crossover probability cross over the parents to form a new offspring (children).
If no crossover was performed, offspring is an exact copy of parents.
"""
def crossover(population, parents):
    random.seed()

    # if we dont crossover, offspring is a copy of parents
    if random.random() > CROSSOVER_RATE:
        return population[parents[0]]
    else:
        # One point crossover
        number = random.random()
        if number < .25:
            return Chromosome(population[parents[1]].kp,population[parents[1]].kd, population[parents[1]].ki)
        elif number < .5:
            return Chromosome(population[parents[0]].kp,population[parents[1]].kd, population[parents[1]].ki)
        elif number < .75:
            return Chromosome(population[parents[0]].kp,population[parents[0]].kd, population[parents[1]].ki)
        else:
            return Chromosome(population[parents[0]].kp,population[parents[0]].kd, population[parents[0]].ki)

"""
3c[Mutation] With a mutation probability mutate new offspring at each locus (position in chromosome).
"""
def mutation(chromosome):
    random.seed()
    rand_number = random.random()

    #very small real valued mutation
    random_mutation = (random.random()-.5)/MAX_GAIN_VALUE

    if rand_number < MUTATION_PROBABILITY / 3:
        if chromosome.kp + random_mutation < 0:
            chromosome.kp = chromosome.kp + math.fabs(random_mutation)
        else:
            chromosome.kp = chromosome.kp + random_mutation
    elif rand_number < MUTATION_PROBABILITY * 2/3:
        if chromosome.ki + random_mutation < 0:
            chromosome.ki = chromosome.ki + math.fabs(random_mutation)
        else:
            chromosome.ki = chromosome.ki + random_mutation
    elif rand_number < MUTATION_PROBABILITY:
        if chromosome.kd + random_mutation < 0:
            chromosome.kd = chromosome.kd + math.fabs(random_mutation)
        else:
            chromosome.kd = chromosome.kd + random_mutation

    return chromosome

"""
3 [New population] Create a new population by repeating following steps until the new population is complete
"""
def generate_new_population(fitness_values, previous_population):
    new_population = []

    # for each child of our new population
    for i in range(POPULATION_SIZE-1):

        # selection
        parents = selection(fitness_values)

        # crossover
        chromosome = crossover(population, parents)


        # mutation
        chromosome = mutation(chromosome)

        # accept
        new_population.append(chromosome)


    """
    Perform hybrid elitist selection. Carry the best chromosome over to the new population, unmutated.
    """
    chromosome = population[listtools.max_index_in_list(fitness_values)]
    new_population.append(chromosome)

    return new_population

