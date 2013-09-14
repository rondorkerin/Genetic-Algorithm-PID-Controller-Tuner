config = {
    'population_size' : 100,
    'mutation_probability' : .1,
    'crossover_rate' : .9,
    # maximum simulation runs before finishing
    'max_runs' : 100,
    # maximum timesteps per simulation
    'max_timesteps' : 150,
    # smoothness value of the line in [0, 1]
    'line_smoothness' : .4,
    # Bound for our gain parameters (p, i, d)
    'max_gain_value' : 3,
    # when set to 1, we create a new map this run. When set to 0, loads a new map
    'new_map' : True,
    'runs_per_screenshot' : 10,
    'data_directory' : '/home/monk/genetic_pid_data',
    'map_filename' : 'map.csv'
}
