import os
import matplotlib.pyplot as plt
from lib.simulation import Simulation
from lib import listtools
from config import config

if not os.path.exists(config['data_directory']):
    os.makedirs(config['data_directory'])

simulation = Simulation(config)
simulation.generate_initial_population()

max_values = []
avg_values = []
kp_values = []
kd_values = []
ki_values = []

for i in range(config['max_runs']):
    simulation.generate_new_population()
    fitness_values = simulation.fitness_values
    population = simulation.population

    # Add the champion chromosome to a list of champions for plotting
    index_of_champion = listtools.max_index_in_list(fitness_values)
    kp_values.append(population[index_of_champion].kp)
    kd_values.append(population[index_of_champion].kd)
    ki_values.append(population[index_of_champion].ki)

    # Add the max/average values to lists for plotting
    max_values.append(listtools.max_value_in_list(fitness_values))
    avg_values.append(listtools.avgList(fitness_values))

    print(f"Run {i}: max value {max_values[i]}, avg value {avg_values[i]}")

# Plot fitness results of each run
plt.figure()
plt.plot(range(config['max_runs']), max_values, label=r"Max Value")
plt.plot(range(config['max_runs']), avg_values, label=r"Average Value")
plt.title("Fitness Values Over Time")
plt.legend(loc='lower right')
plt.xlabel("Run")
plt.ylabel("Value")
plt.savefig(os.path.join(config['data_directory'], "fitness_values_over_time.png"), format="png")

# Plot values of parameters for each run
plt.figure()
plt.plot(range(config['max_runs']), kp_values, label=r"Kp")
plt.plot(range(config['max_runs']), kd_values, label=r"Kd")
plt.plot(range(config['max_runs']), ki_values, label=r"Ki")
plt.title("Champion Gain Values Per Run")
plt.legend(loc='center right')
plt.xlabel("Run")
plt.ylabel("Value")
plt.savefig(os.path.join(config['data_directory'], "champion_gain_values_per_run.png"), format="png")

plt.show()
