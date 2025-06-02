import json

def load_primary_mission(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def load_simulated_missions(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)["flights"]
