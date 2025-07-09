import json

def load_settings(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

SETTINGS = load_settings("src/config/config.json")
