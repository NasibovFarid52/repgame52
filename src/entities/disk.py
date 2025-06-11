import pygame
from constants import YELLOW

class Disk(pygame.sprite.Sprite):
    """Класс собираемого диска (музыкальной пластинки)"""
    def __init__(self, x, y):
        super().__init__()
        # Создаем изображение диска
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)  # Желтый круг
        pygame.draw.circle(self.image, (0, 0, 0), (15, 15), 15, 2)  # Черная обводка
        pygame.draw.circle(self.image, (0, 0, 0), (15, 15), 5)  # Центральное отверстие
        self.rect = self.image.get_rect(center=(x, y))