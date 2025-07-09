import numpy as np
import json
import random
from ..config import SETTINGS

def random_map():
    return random.choice(SETTINGS["MAPS"][:-1]) if SETTINGS["MAPS"] else None

def load_map(filename):
    def convert_map_data(map_data):
        rows, cols = map_data["size"]
        grid = np.full((rows, cols), '.', dtype='<U2')

        for vehicle in map_data["vehicles"]:
            name = vehicle["name"]
            r, c = vehicle["row"], vehicle["col"]
            length = vehicle["length"]
            orientation = vehicle["orientation"].upper()

            for i in range(length):
                if orientation == "H":
                    grid[r][c + i] = name
                elif orientation == "V":
                    grid[r + i][c] = name
                else:
                    raise ValueError(f"Unknown orientation: {orientation}")

        return grid

    with open(filename, 'r') as f:
        map_data = json.load(f)
    return convert_map_data(map_data)
