import pygame
import os
from constants import COLLECTIBLES_PATH


class Disk(pygame.sprite.Sprite):


    # Загружаем текстуру один раз при инициализации класса
    _texture_loaded = False
    _disk_texture = None

    @classmethod
    def load_texture(cls):
        if not cls._texture_loaded:
            # Загружаем текстуру диска
            cls._disk_texture = pygame.image.load(os.path.join(COLLECTIBLES_PATH, "disk.png"))
            # Масштабируем до нужного размера
            size = 30  # Размер диска в пикселях
            cls._disk_texture = pygame.transform.scale(cls._disk_texture, (size, size))
            cls._texture_loaded = True


    def __init__(self, x, y):
        super().__init__()

        # Загружаем текстуру при первом создании диска
        if not Disk._texture_loaded:
            Disk.load_texture()

        self.image = Disk._disk_texture
        self.rect = self.image.get_rect(center=(x, y))