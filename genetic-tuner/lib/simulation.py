from map import Map
from algorithm import GeneticAlgorithm
from chromosome import Chromosome
import random

class Simulation:
    def __init__(self, config):
        self.config = config
        self.map = Map(self.config)
        self.algorithm = GeneticAlgorithm(self.config)
        self.generate_initial_population()

    def generate_initial_population(self):
        """
        Generate a random population of n chromosomes (suitable solutions for the problem).
        """
        random.seed()
        self.population = [Chromosome(
            random.random() * self.config['max_gain_value'],
            random.random() * self.config['max_gain_value'],
            random.random() * self.config['max_gain_value']
        ) for _ in range(self.config['population_size'])]

    def generate_new_population(self):
        """
        Generate a new population by repeating the selection, crossover, mutation, and acceptance steps.
        """
        new_population = []
        self.fitness_values = self.calculate_fitness()

        for _ in range(self.config['population_size']):
            # Selection
            parent_indices = self.algorithm.selection(self.fitness_values)

            # Crossover
            chromosome = self.algorithm.crossover(self.population[parent_indices[0]], self.population[parent_indices[1]])

            # Mutation
            chromosome = self.algorithm.mutation(chromosome)
            new_population.append(chromosome)

        self.population = new_population

    def calculate_fitness(self):
        """
        Calculate fitness values of the entire population.
        """
        return [self.run_simulation_for_chromosome(chromosomeIndex) for chromosomeIndex in range(self.config['population_size'])]

    def run_simulation_for_chromosome(self, chromosomeIndex):
        """
        Run simulation for a specific chromosome.

        Returns the fitness function value of the simulation.
        """
        distance_list = self.simulate_chromosome(chromosomeIndex)
        return self.algorithm.fitness(distance_list)

    def simulate_chromosome(self, chromosomeIndex):
        """
        Simulate the movement of a specific chromosome.

        Returns a list of distances for each timestep.
        """
        distance_list = []
        current_position = 0
        last_distance = 0
        current_summation = 0

        for _ in range(self.config['max_timesteps']):
            current_distance = self.map.get(_) - current_position

            # God integrates empirically
            current_summation += current_distance

            new_velocity = (
                self.population[chromosomeIndex].kp * current_distance +
                self.population[chromosomeIndex].kd * (current_distance - last_distance) +
                self.population[chromosomeIndex].ki * current_summation
            )

            current_position += new_velocity
            distance_list.append(current_distance)

            # For the derivative
            last_distance = current_distance

        return distance_list
