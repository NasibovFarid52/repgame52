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
            data = json.load(f)

        # Создаем группы спрайтов
        platforms = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        disks = pygame.sprite.Group()

        # Загрузка платформ
        for plat in data["platforms"]:
            p = Platform(
                plat["x"],
                plat["y"],
                plat["width"],
                plat["height"],
                plat.get("type", "static")
            )
            platforms.add(p)

        # Загрузка врагов
        for enemy in data["enemies"]:
            if enemy["type"] == "rat":
                e = Rat(enemy["x"], enemy["y"], platforms)
            elif enemy["type"] == "policeman":
                e = Policeman(enemy["x"], enemy["y"], platforms, enemy.get("direction", 1))
            enemies.add(e)

        # Загрузка дисков
        for disk in data["disks"]:
            d = Disk(disk["x"], disk["y"])
            disks.add(d)

        # Позиция игрока
        player_start = (data["player"]["x"], data["player"]["y"])

        return {
            "platforms": platforms,
            "enemies": enemies,
            "disks": disks,
            "player_start": player_start
        }
    except Exception as e:
        print(f"Ошибка загрузки уровня {level_num}: {e}")
        return None