from map import Map
from algorithm import GeneticAlgorithm
from chromosome import Chromosome
import random

"""
    Main

    1 [Start] Generate random population of n chromosomes (suitable solutions for the problem)
    2 [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
    3 [New population] Create a new population by repeating following steps until the new population is complete
        3a[Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
        3b[Crossover] With a crossover probability cross over the parents to form a new offspring (children). If no crossover was performed, offspring is an exact copy
        3c[Mutation] With a mutation probability mutate new offspring at each locus (position in chromosome).
        3d[Accepting] Place new offspring in a new population
    4 [Replace] Use new generated population for a further run of algorithm
    5 [Test] If the end condition is satisfied, stop, and return the best solution in current population
    6 [Loop] Go to step 2
"""
class Simulation:
    def __init__(self, config):
        self.config = config
        self.map = Map(self.config)
        self.algorithm = GeneticAlgorithm(self.config)
        self.generate_initial_population()

    def generate_initial_population(self):
        """
        Generate random population of n chromosomes (suitable solutions for the problem)
        Creates a random genome
        """
        random.seed()
        self.population = []
        for chromosome in range(self.config['population_size']):
            # create a random chromosome with a random gain value
            self.population.append(Chromosome(random.random() * self.config['max_gain_value'], random.random() * self.config['max_gain_value'], random.random() * self.config['max_gain_value']))

    """
    3 [New population] Create a new population by repeating following steps until the new population is complete
    """
    def generate_new_population(self):
        new_population = []
        for i in range(self.self.config['population_size']-1):
            # selection
            parents = self.algorithm.selection(self.fitness_values)

            # crossover
            chromosome = self.algorithm.crossover(self.population, parents)

            # mutation
            chromosome = self.algorithm.mutation(chromosome)
            new_population.append(chromosome)

        return new_population

    def run_one_generation(self):
        self.fitness_values = []
        for chromosome in range(self.config['population_size']):
            self.fitness_values.append(chromosome)
            self.fitness_values[chromosome] = run_simulation_for_chromosome(map, population, chromosome)


    def run_simulation_for_chromosome(map, population, chromosome):
        """
        Run simulation for a specific chromosome c.

        Returns the fitness function value of the simulation
        """

        distance_list = []
        current_position = 0
        last_distance = 0
        current_summation = 0
        current_distance = 0

        for time in range(MAX_TIMESTEPS):
            distance_list.append(time)
            current_distance = map[time] - current_position

            #for integral controller
            current_summation = current_summation + current_distance

            new_velocity = population[chromosome].kp * current_distance + population[chromosome].kd * (current_distance-last_distance) + population[chromosome].ki * current_summation
            #x = x + dx/dt * dt (dt = 1)

            current_position = current_position + new_velocity

            distance_list[time] = current_distance

            # for the derivative
            last_distance = current_distance

        return self.algorithm.fitness(distance_list)


