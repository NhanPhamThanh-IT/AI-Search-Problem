import json
from .vehicle import Vehicle
from .board import Board

def load_map_from_json(path):
    with open(path) as f:
        data = json.load(f)
    return create_board_from_dict(data)

def create_board_from_dict(data):
    size = tuple(data["size"])
    vehicles = [
        Vehicle(v["name"], v["row"], v["col"], v["length"], v["orientation"])
        for v in data["vehicles"]
    ]
    return Board(size, vehicles)
