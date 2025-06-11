import pygame
from constants import PURPLE

class Door(pygame.sprite.Sprite):
    """Класс двери для перехода на следующий уровень"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 100))
        self.image.fill(PURPLE)
        # Рисуем дверную ручку
        pygame.draw.circle(self.image, (255, 215, 0), (45, 50), 5)  # Золотая ручка
        self.rect = self.image.get_rect(topleft=(x, y))