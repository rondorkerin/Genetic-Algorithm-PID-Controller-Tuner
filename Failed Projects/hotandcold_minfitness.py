import random
import math
import listtools
import csv

#
#
# Which one converges faster, elitism or non-elitism?
# Does it converge faster when we make sure we grab two distinct parents?
#
# Take 2: Instead of encoding a two dimensional array of bits, we encode bits ina  one dimensional array
#
# "A hybrid genetic algorithm for sequence dependent flow shop scheduling problem" by muhammad marabi <-- we used this for our idea of checking for better fit children.

# abandoned due to improper encoding

# enumerations for different actions to be taken
MOVE_POSITION = 0
HOLD_POSITION = 1

# enumerations for different states of the map
# TODO: COLD/HOT
COLD, HOT = range(2)

MAX_DISTANCE = 100
MAX_TIMESTEPS = 1000
POPULATION_SIZE = 100
MUTATION_PROBABILITY = .01
CROSSOVER_RATE = .7
MAX_RUNS = 100000

"""
Creates a map up to 200 timesteps ( can be increased )

format: map[pos][time] = PASS or KILL
"""
def create_map():
	random.seed()
	map = []
	
	for pos in range(MAX_DISTANCE):
		map.append(pos)
		times = []
		for time in range(MAX_TIMESTEPS):
			# .8 probability that any given tile at a given timestep will be "pass"
			if random.random() < .3:
				times.append(COLD)
			else:
				times.append(HOT)
		map[pos] = times
	return map
	
"""
1 [Start] Generate random population of n chromosomes (suitable solutions for the problem)
Creates a random genome

format: population[chromosome][time] = MOVE or HOLD
"""
def generate_initial_population():
	random.seed()
	population = []
	for chromosome in range(POPULATION_SIZE):
		population.append(chromosome)
		times = []
		for t in range(MAX_TIMESTEPS):
			times.append(math.floor(random.random()*2))
		population[chromosome] = times
	return population
		
""" 
2 [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
returns the fitness value according to the fitness function

Attempt to minimize fitness value.
"""
def fitness(timesteps, sum_hot, sum_cold):
	f = math.fabs(sum_hot - sum_cold)
	return f		
		
"""
Run simulation for a specific chromosome c.

At timestep t and  position p, 

Returns the fitness function value of the simulation
"""
def run_simulation_for_chromosome(map, population, chromosome):
	current_position = 0
	sum_hot = 0
	sum_cold = 0
	for time in range(MAX_TIMESTEPS):
		if current_position == MAX_DISTANCE-1:
			return fitness(time, sum_hot, sum_cold)
		if population[chromosome][time] == MOVE_POSITION:
			current_position = current_position + 1
			
		if map[current_position][time] == COLD:
			sum_cold = sum_cold + 1
		else:
			sum_hot = sum_hot + 1
				
	# the agent has waited too long and is penalized maximally
	return 9999999

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
3a[Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)

returns the chromosome indices of the chosen parents

"""
"""
def selection(fitness_values):
# This is elitism
	parents = []
	random.seed()
	minVal = 9999999
	minIndex = 0
	for i in range(POPULATION_SIZE):
		if fitness_values[i] < minVal:
			minVal = fitness_values[i]
			minIndex = i
	parents.append(minIndex)
	minVal2 = 9999999
	minIndex2 = 0
	for i in range(POPULATION_SIZE):
		if fitness_values[i] < minVal2 and i != minIndex:
			minIndex2 = i
			minVal2 = fitness_values[i]
	parents.append(minIndex2)
	
	return parents

"""

def selection(fitness_values):
	# normalize the list so we have probabilities to pick parents
	probabilities = []
	for i in range(len(fitness_values)):
		probabilities.append(i)
		probabilities[i] = 1 / (fitness_values[i] + 1)
	probabilities = listtools.normListSumTo(probabilities, 1)
	parents = []
	random.seed()
	parent1_probability = random.random()
	parent2_probability = random.random()
	
	sum = 0
	for i in range(POPULATION_SIZE):
		if len(parents) == 2:
			break
		next_sum = sum + probabilities[i]
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
	if random.random() < CROSSOVER_RATE:
		return population[parents[0]]
	
	# this will be the new chromosome
	times = []
	
	"""
	# wait until the two parents no longer match before crossing over (since we're sequence-dependent)
	match_timestep = MAX_TIMESTEPS
	for t in range(MAX_TIMESTEPS):
		if population[parents[0]][t] == population[parents[1]][t]:
			#add the matching chromosome to the new chromosome
			times.append(t)
			times[t] = population[parents[0]][t]
		else:
			match_timestep = t + 1
			break
	"""
	
	
	crossover_time = math.floor(random.random() * (MAX_TIMESTEPS))

	for t in range(MAX_TIMESTEPS):
		times.append(t)
		if t > crossover_time:
			times[t] = population[parents[0]][t]
		else:
			times[t] = population[parents[1]][t]

	return times
	
"""
3c[Mutation] With a mutation probability mutate new offspring at each locus (position in chromosome).
"""
def mutation(times):
	random.seed()
	
	for t in range(MAX_TIMESTEPS):
		if random.random() > MUTATION_PROBABILITY:
			times[t] = math.floor(random.random()*2)
		
	return times
	
"""
3 [New population] Create a new population by repeating following steps until the new population is complete
"""
def generate_new_population(fitness_values, previous_population):
	new_population = []
	for i in range(POPULATION_SIZE):
		new_population.append(i)
		# selection
		parents = selection(fitness_values)

		# crossover
		times = crossover(population, parents)

		# mutation
		times = mutation(times)
		new_population[i] = times
	
	return new_population
	
	
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
	
#################################################################################################################################################
#  	
#  	NOTE: Fitness_values is indexed by chromosome number, so if we attempt to sort it, 
#   we will pick the wrong index when generating a new population. Which would be bad.
#
#################################################################################################################################################
map = create_map()
population = generate_initial_population()
fitness_values = run_simulation(map, population)

# write out our results to a csv for graphing
csvWriter = csv.writer(open('geneticalgo.csv', 'wb'), delimiter=',',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
for i in range(MAX_RUNS):
	population = generate_new_population(fitness_values, population)
	fitness_values = run_simulation(map, population)
	
	min_value = listtools.min_value_in_list(fitness_values)
	avg_value = listtools.avgList(fitness_values)

	csvWriter.writerow([avg_value, min_value])
	print "Run " + str(i) + ":  avg value " + str(avg_value) + ", min value " + str(min_value)
	# currently our function evaluates to distance so max distance is true.
	if  min_value == 0:
		print "SOLUTION FOUND."
		break
