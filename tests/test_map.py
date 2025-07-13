# give me the code to check the valid positions of vehicles in a map (from src/maps folder)
# File: src/maps/map10.json
# This file defines a map with vehicles and their positions.
# The vehicles are represented by their names, positions (row and column), lengths, and orientations
# The map size is defined as a list with two elements: number of rows and columns.
# {
#   "size": [6, 6],
#   "vehicles": [
#     { "name": "A", "row": 0, "col": 3, "length": 2, "orientation": "H" },
#     { "name": "B", "row": 1, "col": 1, "length": 2, "orientation": "H" },
#     { "name": "C", "row": 1, "col": 4, "length": 2, "orientation": "V" },
#     { "name": "D", "row": 1, "col": 5, "length": 2, "orientation": "V" },
#     { "name": "E", "row": 4, "col": 0, "length": 2, "orientation": "H" },
#     { "name": "F", "row": 4, "col": 2, "length": 2, "orientation": "V" },
#     { "name": "G", "row": 3, "col": 4, "length": 2, "orientation": "H" },
#     { "name": "X", "row": 2, "col": 0, "length": 2, "orientation": "H" }
#   ]
# }

import os
import json

def check_valid_positions(map_data):
    size = map_data['size']
    vehicles = map_data['vehicles']
    
    # Create a grid to represent the map
    grid = [[None for _ in range(size[1])] for _ in range(size[0])]
    
    for vehicle in vehicles:
        row, col, length, orientation = vehicle['row'], vehicle['col'], vehicle['length'], vehicle['orientation']
        
        if orientation == 'H':
            if col + length > size[1]:
                return False
            for c in range(col, col + length):
                if grid[row][c] is not None:
                    return False
                grid[row][c] = vehicle['name']
        else:
            if row + length > size[0]:
                return False
            for r in range(row, row + length):
                if grid[r][col] is not None:
                    return False
                grid[r][col] = vehicle['name']
    
    return True

# Example usage
if __name__ == "__main__":
    maps_folders = os.listdir('../src/maps')
    for map_file in maps_folders:
        with open(f'../src/maps/{map_file}') as f:
            map_data = json.load(f)
            is_valid = check_valid_positions(map_data)
            print(f'Map {map_file} is valid: {is_valid}')