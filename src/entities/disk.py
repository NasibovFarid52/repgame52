import pygame
import os
from constants import COLLECTIBLES_PATH, YELLOW


class Disk(pygame.sprite.Sprite):
    """Класс собираемого диска"""

    # Загружаем текстуру один раз при инициализации класса
    _texture_loaded = False
    _disk_texture = None

    @classmethod
    def load_texture(cls):
        """Загружает текстуру диска из файла"""
        if not cls._texture_loaded:
            try:
                # Загружаем текстуру диска
                cls._disk_texture = pygame.image.load(os.path.join(COLLECTIBLES_PATH, "disk.png"))
                # Масштабируем до нужного размера
                size = 30  # Размер диска в пикселях
                cls._disk_texture = pygame.transform.scale(cls._disk_texture, (size, size))
                cls._texture_loaded = True
            except Exception as e:
                print(f"Ошибка загрузки текстуры диска: {e}")
                # Создаем простой диск, если текстура не загружена
                cls._disk_texture = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.circle(cls._disk_texture, YELLOW, (15, 15), 15)
                pygame.draw.circle(cls._disk_texture, (0, 0, 0), (15, 15), 15, 2)
                pygame.draw.circle(cls._disk_texture, (0, 0, 0), (15, 15), 5)

    def __init__(self, x, y):
        super().__init__()

        # Загружаем текстуру при первом создании диска
        if not Disk._texture_loaded:
            Disk.load_texture()

        self.image = Disk._disk_texture
        self.rect = self.image.get_rect(center=(x, y))