import json
import random
from config import SETTINGS
from core import Board, Vehicle

def random_map():
    return random.choice(SETTINGS["MAPS"][:-1]) if SETTINGS["MAPS"] else None

def load_map_from_json(json_data: str) -> Board:
    data = json.loads(json_data)
    board_size = tuple(data["size"])
    vehicles_data = data["vehicles"]

    vehicles = {}

    for v in vehicles_data:
        name = v["name"]
        row = v["row"]
        col = v["col"]
        length = v["length"]
        orientation = v["orientation"]
        vehicles[name] = Vehicle(name, row, col, length, orientation)

    return Board(board_size, vehicles)
