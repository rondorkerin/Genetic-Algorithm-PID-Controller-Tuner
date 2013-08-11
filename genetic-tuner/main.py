import random
import math
import csv
import matplotlib.pyplot as plt
import os
from lib.chromosome import Chromosome
from lib import listtools
from lib.genetic_pid import *

"""
Genetic algorithm for tuning a 1 dimensional pid controller
"""

# Genetic algorithm parameters

POPULATION_SIZE = 100
MUTATION_PROBABILITY = .1
CROSSOVER_RATE = .9
MAX_RUNS = 100

# Simulation Parameters
MAX_TIMESTEPS = 150
LINE_SMOOTHNESS = .1
MAX_GAIN_VALUE = 3

# Control Variables
# when set to 1, we create a new map this run. When set to 0, loads a new map
NEW_MAP = 1
# The number of runs we wait between showing a screenshot of the champion's run
RUNS_PER_SCREENSHOT = 10

#http://www.waset.org/journals/waset/v56/v56-89.pdf
# Premature convergence problem.
#

"""
Creates a map based on a line smoothness. The smoother the line, the less jagged it will become
"""
def create_map():
    random.seed()
    map = []

    current_map_value = 0

    csvWriter = csv.writer(open('map.csv', 'wb'), delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for time in range(MAX_TIMESTEPS):
        # the smaller LINE_SMOOTHNESS, the more smooth the line is
        if random.random() < LINE_SMOOTHNESS:
            map.append(current_map_value + (random.random() - .5)*MAX_GAIN_VALUE/1000)
        else:
            map.append(current_map_value)
        current_map_value = map[time]
        csvWriter.writerow([current_map_value])

    return map


"""
Loads the local file map.csv into a line.
"""
def load_map():
    list_map = list(csv.reader(open("map.csv", "rb")))
    map = []
    for time in range(len(list_map)):
        map.append(float(list_map[time]))
    return map

"""
    Main

    1 [Start] Generate random population of n chromosomes (suitable solutions for the problem)
    2 [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
    3 [New population] Create a new population by repeating following steps until the new population is complete
        3a[Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
        3b[Crossover] With a crossover probability cross over the parents to form a new offspring (children). If no crossover was performed, offspring is an exact copy of parents.
        3c[Mutation] With a mutation probability mutate new offspring at each locus (position in chromosome).
        3d[Accepting] Place new offspring in a new population
    4 [Replace] Use new generated population for a further run of algorithm
    5 [Test] If the end condition is satisfied, stop, and return the best solution in current population
    6 [Loop] Go to step 2
"""

# create map or load map based on mode
if NEW_MAP == 1:
    map = create_map()
else:
    map = load_map()

# make a directory to store results
try:
    os.mkdir("results")
except OSError:
    pass

population = generate_initial_population()
fitness_values = run_simulation(map, population)

max_values = []
avg_values = []
kp_values = []
kd_values = []
ki_values = []

# perform simulation

for i in range(MAX_RUNS):

    # generate population and run the simulation
    population = generate_new_population(fitness_values, population)
    fitness_values = run_simulation(map, population)

    # add the champion chromosome to a list of champions for plotting
    index_of_champion = listtools.max_index_in_list(fitness_values)
    kp_values.append(population[index_of_champion].kp)
    kd_values.append(population[index_of_champion].kd)
    ki_values.append(population[index_of_champion].ki)


    # add the max/average values to lists for plotting
    max_values.append(listtools.max_value_in_list(fitness_values))
    avg_values.append(listtools.avgList(fitness_values))


    # every RUNS_PER_SCREENSHOT runs, do a plot of the champion chromosome
    if i % RUNS_PER_SCREENSHOT == 0:
        # run the simulation for the first selected parent
        run_simulation_for_champion(map, population, index_of_champion, i, listtools.max_value_in_list(fitness_values))

    print "Run " + str(i) + ": max value " + str(max_values[i]) + ", avg value " + str(avg_values[i])


# plot fitness results of each run

plt.figure()
plt.plot()
plt.title("Fitness Values Over Time")

plt.plot(range(MAX_RUNS), max_values, label = r"Max Value")
plt.plot(range(MAX_RUNS), avg_values, label = r"Average Value")
plt.legend(loc='lower right')
plt.xlabel("Run")
plt.ylabel("Value")
plt.savefig("results/fitness_values_over_time.png", format="png")

# plot values of parameters for each run
plt.figure()
plt.plot()
plt.title("Champion Gain Values Per Run")

plt.plot(range(MAX_RUNS), kp_values, label = r"Kp")
plt.plot(range(MAX_RUNS), kd_values, label = r"Kd")
plt.plot(range(MAX_RUNS), ki_values, label = r"Ki")
plt.legend(loc='center right')
plt.xlabel("Run")
plt.ylabel("Value")
plt.savefig("results/champion_gain_values_per_run.png", format="png")
