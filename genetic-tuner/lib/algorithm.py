import random
import math
from chromosome import Chromosome
from listtools import normListSumTo

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config

    def mutation(self, chromosome):
        """
        Mutate the chromosome with a mutation probability at each locus.
        """
        max_gain_value = self.config['max_gain_value']
        mutation_probability = self.config['mutation_probability']

        def apply_mutation(gene, mutation_prob):
            if random.random() < mutation_prob:
                gene += random.random() / max_gain_value
            if gene < 0:
                gene = random.random() * max_gain_value
            return gene

        chromosome.kp = apply_mutation(chromosome.kp, mutation_probability / 3)
        chromosome.ki = apply_mutation(chromosome.ki, mutation_probability * 2 / 3)
        chromosome.kd = apply_mutation(chromosome.kd, mutation_probability)

        return chromosome

    def crossover(self, parent1, parent2):
        """
        Perform crossover to form a new offspring (child).
        """
        if random.random() > self.config['crossover_rate']:
            return parent1
        else:
            crossover_types = [
                (parent1.kp, parent1.kd, parent1.ki),
                (parent2.kp, parent1.kd, parent1.ki),
                (parent1.kp, parent2.kd, parent1.ki),
                (parent1.kp, parent1.kd, parent2.ki),
                (parent2.kp, parent1.kd, parent2.ki),
                (parent2.kp, parent2.kd, parent2.ki)
            ]
            return Chromosome(*random.choice(crossover_types))

    def selection(self, fitness_values):
        """
        Select two parent indices based on normalized fitness values.
        """
        fitness_values = normListSumTo(fitness_values, 1)
        parent_indices = random.choices(range(len(fitness_values)), weights=fitness_values, k=2)
        return parent_indices

    def fitness(self, distance_list):
        """
        Evaluate the fitness of each chromosome in the population.
        """
        sum_squares = sum(distance ** 2 for distance in distance_list)
        return 1 / math.sqrt(sum_squares)
