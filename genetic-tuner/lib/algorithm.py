import random
import math
import listtools
from chromosome import Chromosome

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config

    def mutation(self, chromosome):
        """
        With a mutation probability mutate new offspring at each locus (position in chromosome).
        """
        random.seed()
        #very small real valued mutation
        max_gain_value = self.config['max_gain_value']

        if random.random() < self.config['mutation_probability'] / 3:
            chromosome.kp = chromosome.kp + random.random()/max_gain_value
        if chromosome.kp < 0:
            chromosome.kp = random.random() * max_gain_value

        elif random.random() < self.config['mutation_probability'] * 2/3:
            chromosome.ki = chromosome.ki + random.random()/max_gain_value
        if chromosome.ki < 0:
            chromosome.ki = random.random() * max_gain_value

        elif random.random() < self.config['mutation_probability']:
            chromosome.kd = chromosome.kd + random.random()/max_gain_value
        if chromosome.kd < 0:
            chromosome.kd = random.random() * max_gain_value

        return chromosome

    def crossover(self, parent1, parent2):
        """
        3b[Crossover] With a crossover probability cross over the parents to form a new offspring (children).
        If no crossover was performed, offspring is an exact copy of parents.
        """
        random.seed()

        # if we dont crossover, offspring is a copy of parents
        if random.random() > self.config['crossover_rate']:
            return parent1
        else:
            # random combination crossover
            number = random.random()
            if number < 1.0/6:
                return Chromosome(parent1.kp,parent1.kd, parent1.ki)
            elif number < 2.0/6:
                return Chromosome(parent2.kp, parent1.kd, parent1.ki)
            elif number < 3.0/6:
                return Chromosome(parent1.kp, parent2.kd, parent1.ki)
            elif number < 4.0/6:
                return Chromosome(parent1.kp, parent1.kd, parent2.ki)
            elif number < 5.0/6:
                return Chromosome(parent2.kp,parent1.kd, parent2.ki)
            else:
                return Chromosome(parent2.kp,parent2.kd, parent2.ki)

    def selection(self, fitness_values):
        """
        Pick two parents according to probability represented by normalized fitness values
        3a[Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
        """
        # normalize the list so we have probabilities to pick parents
        fitness_values = listtools.normListSumTo(fitness_values, 1)
        parentIndices = []
        random.seed()
        parent1_probability = random.random()
        parent2_probability = random.random()

        sum = 0
        for i in range(self.config['population_size']):
            if len(parentIndices) == 2:
                break
            next_sum = sum + fitness_values[i]
            if parent1_probability <= next_sum and parent1_probability >= sum:
                parentIndices.append(i)
            if parent2_probability <= next_sum and parent2_probability >= sum:
                parentIndices.append(i)
            sum = next_sum
        return parentIndices

    def fitness(self, distance_list):
        """
        Evaluate the fitness f(x) of each chromosome x in the population
        returns the fitness value according to the fitness function

        f(x): takes in a list of distances, finds the sum of their squares and returns the inverse of it.
        """
        sum = 0
        for i in range(len(distance_list)):
            sum = sum + distance_list[i]**2
        return 1 /  math.sqrt(sum)


