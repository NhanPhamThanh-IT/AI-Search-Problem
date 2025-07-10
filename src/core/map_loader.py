import json
from core.board import Board

def load_map_from_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return Board.from_dict(data)
