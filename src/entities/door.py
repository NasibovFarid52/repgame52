import pygame
import os
from constants import DOORS_PATH, PURPLE


class Door(pygame.sprite.Sprite):
    """Класс двери для перехода на следующий уровень"""

    # Загружаем текстуру один раз при инициализации класса
    _texture_loaded = False
    _door_texture = None

    @classmethod
    def load_texture(cls):
        """Загружает текстуру двери из файла"""
        if not cls._texture_loaded:
            try:
                # Загружаем текстуру двери
                cls._door_texture = pygame.image.load(os.path.join(DOORS_PATH, "door.png"))
                # Масштабируем до нужного размера
                width, height = 60, 100  # Размер двери
                cls._door_texture = pygame.transform.scale(cls._door_texture, (width, height))
                cls._texture_loaded = True
            except Exception as e:
                print(f"Ошибка загрузки текстуры двери: {e}")
                # Создаем простую дверь, если текстура не загружена
                cls._door_texture = pygame.Surface((60, 100))
                cls._door_texture.fill(PURPLE)
                # Рисуем дверную ручку
                pygame.draw.circle(cls._door_texture, (255, 215, 0), (45, 50), 5)

    def __init__(self, x, y):
        super().__init__()

        # Загружаем текстуру при первом создании двери
        if not Door._texture_loaded:
            Door.load_texture()

        self.image = Door._door_texture
        self.rect = self.image.get_rect(topleft=(x, y))