import os
import json
import random
from config import SETTINGS
from core import Board, Vehicle

def random_map():
    """
    Select a random map from the available maps in SETTINGS.
    
    Returns:
        str: Name of the randomly selected map, or None if no maps are available.
    """
    return random.choice(SETTINGS["MAPS"][:-1]) if SETTINGS["MAPS"] else None

def load_map_from_json(json_data: str) -> Board:
    """
    Load a map from a JSON string and return a Board object.
    
    Args:
        json_data (str): JSON string containing map data.
    
    Returns:
        Board: A Board object initialized with the map data.
    
    Raises:
        ValueError: If the JSON data is invalid or does not contain the expected structure.
    """
    data = json.loads(json_data)
    board_size = tuple(data["size"])
    vehicles_data = data["vehicles"]

    # Reset màu trước khi tạo vehicles mới
    Vehicle.reset_colors()
    vehicles = {}

    for v in vehicles_data:
        name = v["name"]
        row = v["row"]
        col = v["col"]
        length = v["length"]
        orientation = v["orientation"]
        vehicles[name] = Vehicle(name, row, col, length, orientation)

    return Board(board_size, vehicles)

def get_list_maps(folder_path: str) -> list:
    """
    Get a list of map filenames from the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing map files.
    
    Returns:
        list: List of map filenames with .json extension.
    """
    maps = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            maps.append(filename)
    return maps