class Config:
    def __init__(self):
        self.population_size = 100
        self.mutation_probability = 0.1
        self.crossover_rate = 0.9
        self.max_runs = 100
        self.max_timesteps = 150
        self.line_smoothness = 0.4
        self.max_gain_value = 3
        self.new_map = True
        self.runs_per_screenshot = 10
        self.data_directory = '/home/monk/genetic_pid_data'
        self.map_filename = 'map.csv'

# Create an instance of the Config class
config = Config()
