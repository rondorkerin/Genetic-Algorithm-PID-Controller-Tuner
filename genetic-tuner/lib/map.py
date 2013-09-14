import random
import csv
import os
"""
Map is a list of float values that randomly walk around the center point (0)
There is one point for each timestep in the simulation
"""
class Map:
    def __init__(self, config):
        filePath = os.path.join(config['data_directory'], config['map_filename'])
        if config['new_map']:
            self.createNew(filePath, config['max_timesteps'], config['line_smoothness'])
        else:
            self.load(filePath)

    """
    Creates a map based on a line smoothness. The smoother the line, the less jagged it will become
    Smoothness varies between [0 and 1] with 0 being the smoothest
    """
    def createNew(self, filePath, maxTimesteps, lineSmoothness):
        random.seed()
        map = []

        current_map_value = 0

        csvWriter = csv.writer(open(filePath, 'wb'), delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for time in range(maxTimesteps):
            # the smaller lineSmoothness, the more smooth the line is
            if random.random() < lineSmoothness:
                map.append(current_map_value + (random.random() - .5)/1000)
            else:
                map.append(current_map_value)
            current_map_value = map[time]
            csvWriter.writerow([current_map_value])

        self.map = map

    """
    Loads the local file map.csv into a line.
    """
    def load(self, filePath):
        list_map = list(csv.reader(open(filePath, "rb")))
        map = []
        for time in range(len(list_map)):
            map.append(float(list_map[time]))

        self.map = map

    def get(self, index):
        return self.map[index]


