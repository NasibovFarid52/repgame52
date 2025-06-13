import pygame
import json
import os
from constants import LEVELS_PATH
from src.entities.platform import Platform
from src.entities.rat import Rat
from src.entities.policeman import Policeman
from src.entities.disk import Disk


def load_level(level_num):
    """Загружает уровень из файла (DRY - переиспользуемый загрузчик)"""
    filename = os.path.join(LEVELS_PATH, f"level{level_num}.json")
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки уровня {level_num}: {e}")
        return None