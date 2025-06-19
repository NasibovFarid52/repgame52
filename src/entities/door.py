import pygame
import os
from constants import DOORS_PATH


class Door(pygame.sprite.Sprite):


    # Загружаем текстуру один раз при инициализации класса
    _texture_loaded = False
    _door_texture = None

    @classmethod
    def load_texture(cls):
        if not cls._texture_loaded:
            # Загружаем текстуру двери
            cls._door_texture = pygame.image.load(os.path.join(DOORS_PATH, "door.png"))
            # Масштабируем до нужного размера
            width, height = 60, 100  # Размер двери
            cls._door_texture = pygame.transform.scale(cls._door_texture, (width, height))
            cls._texture_loaded = True


    def __init__(self, x, y):
        super().__init__()

        # Загружаем текстуру при первом создании двери
        if not Door._texture_loaded:
            Door.load_texture()

        self.image = Door._door_texture
        self.rect = self.image.get_rect(topleft=(x, y))