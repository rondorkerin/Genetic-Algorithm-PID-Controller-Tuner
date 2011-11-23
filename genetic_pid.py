import random
import math
import listtools
import csv

#
# Genetic algorithm for tuning a 1 dimensional pid controller
#

MAX_TIMESTEPS = 150
POPULATION_SIZE = 100
MUTATION_PROBABILITY = .1
CROSSOVER_RATE = .9
MAX_RUNS = 100
FITNESS_THRESHOLD = .00001
MAX_GAIN_VALUE = .1
LINE_SMOOTHNESS = .1
#DYNAMIC_FACTOR = .01

#http://www.waset.org/journals/waset/v56/v56-89.pdf
# Premature convergence problem.
#

class Chromosome:
	def __init__(self, kp, kd, ki):
		self.kp = kp
		self.kd = kd
		self.ki = ki
	 
"""

"""
def create_map():
	random.seed()
	map = []
	
	current_map_value = 0
	
	csvWriter = csv.writer(open('map.csv', 'wb'), delimiter=',',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
	
	for time in range(MAX_TIMESTEPS):
		map.append(time)
		# the smaller LINE_SMOOTHNESS, the more smooth the line is
		if random.random() < LINE_SMOOTHNESS:
			map[time] = current_map_value + (random.random() - .5)*MAX_GAIN_VALUE/1000
		else:
			map[time] = current_map_value
		current_map_value = map[time]
		csvWriter.writerow([current_map_value])

	return map
	
def load_map():
# http://love-python.blogspot.com/2008/02/read-csv-file-in-python.html
	list_map = list(csv.reader(open("map.csv", "rb")))
	map = []
	for time in range(len(list_map)):
		map.append(time)
		map[time] = float(list_map[time][0])
	return map
	
		
	
"""
1 [Start] Generate random population of n chromosomes (suitable solutions for the problem)
Creates a random genome

"""
def generate_initial_population():
	random.seed()
	population = []
	for chromosome in range(POPULATION_SIZE):
		# create a random chromosome with a random gain value
		population.append(chromosome)
		population[chromosome] = Chromosome(random.random() * MAX_GAIN_VALUE, random.random() * MAX_GAIN_VALUE, random.random() * MAX_GAIN_VALUE)
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
		distance_list.append(time)
		current_distance = map[time] - current_position
	
		#for integral controller
		current_summation = current_summation + current_distance
		
		new_velocity = population[chromosome].kp * current_distance + population[chromosome].kd * (current_distance-last_distance) + population[chromosome].ki * current_summation
		
		#simulate dynamic environment
		#new_velocity = new_velocity * (1 + random.random()*DYNAMIC_FACTOR)
		#x = x + dx/dt * dt (dt = 1)
		
		current_position = current_position + new_velocity
		
		distance_list[time] = current_distance
			
		# for the derivative
		last_distance = current_distance
	
	return fitness(distance_list)
	
			
"""
Run simulation for a specific chromosome c.

Returns the fitness function value of the simulation
"""
def run_simulation_for_best(map, population, chromosome, runNumber, fitness_factor):
	
	distance_list = []
	current_position = 0
	last_distance = 0
	current_summation = 0
	current_distance = 0
					
	csvWriter = csv.writer(open('best_run' + str(runNumber) + '.csv', 'wb'), delimiter=',',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
						
	csvWriter.writerow(['fitness ', fitness_factor])
	csvWriter.writerow(['kp', population[chromosome].kp])
	csvWriter.writerow(['kd', population[chromosome].kd])
	csvWriter.writerow(['ki', population[chromosome].ki])
	csvWriter.writerow(['position: ', 'line position'])					
					
	for time in range(MAX_TIMESTEPS):
		distance_list.append(time)
		current_distance = map[time] - current_position
		#for integral controller
		current_summation = current_summation + current_distance
		
		new_velocity = population[chromosome].kp * current_distance + population[chromosome].kd * (current_distance-last_distance) + population[chromosome].ki * current_summation
		# find the v = (x2-x1)*kp and x = x + dx/dt * dt (dt = 1)
	
		#simulate dynamic environment
		#new_velocity = new_velocity * (1 + random.random()*DYNAMIC_FACTOR)
	
		current_position = current_position + new_velocity
			
		csvWriter.writerow([current_position, map[time]])
		
		distance_list[time] = current_distance
			
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
3a[Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
"""
def selection(fitness_values):
	# normalize the list so we have probabilities to pick parents
	fitness_values = listtools.normListSumTo(fitness_values, 1)
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
		# random combination crossover
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
	for i in range(POPULATION_SIZE-1):
		new_population.append(i)
		# selection
		parents = selection(fitness_values)
				
		# crossover
		chromosome = crossover(population, parents)

		# mutation
		chromosome = mutation(chromosome)
		new_population[i] = chromosome
	
	
	"""
	Perform hybrid elitist selection. Carry the best chromosome over to the new population, unmutated.
	"""
	chromosome = population[listtools.max_index_in_list(fitness_values)]
	new_population.append(POPULATION_SIZE-1)
	new_population[POPULATION_SIZE-1] = chromosome
	
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
# create map or load map based on debug mode
#map = create_map()
map = load_map()
population = generate_initial_population()
fitness_values = run_simulation(map, population)


# write out our results to a csv for graphing
csvWriter = csv.writer(open('geneticalgo.csv', 'wb'), delimiter=',',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
for i in range(MAX_RUNS):
	population = generate_new_population(fitness_values, population)
	fitness_values = run_simulation(map, population)
	
	if i % 10 == 0:
		# run the simulation for the first selected parent
		run_simulation_for_best(map, population, listtools.max_index_in_list(fitness_values), i, listtools.max_value_in_list(fitness_values))
	
	max_value = listtools.max_value_in_list(fitness_values)
	avg_value = listtools.avgList(fitness_values)
	
	# if the population sucks, DESTROY THE EARTH
	if max_value < FITNESS_THRESHOLD:
		population = generate_initial_population()
		continue

	csvWriter.writerow([avg_value, max_value])
	print "Run " + str(i) + ": max value " + str(max_value) + ", avg value " + str(avg_value)

		
	
