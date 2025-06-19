import json
import os
from constants import LEVELS_PATH


def load_level(level_num):
    filename = os.path.join(LEVELS_PATH, f"level{level_num}.json")
    with open(filename, 'r') as f:
        return json.load(f)
