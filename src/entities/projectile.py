import pygame

from constants import SCREEN_WIDTH


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Красная пуля
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.x += self.speed * self.direction
        # Удаление пули при выходе за пределы экрана
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()