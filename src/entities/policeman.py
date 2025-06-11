import pygame
import random
from constants import BLUE, GRAVITY
from src.entities.projectile import Projectile


class Policeman(pygame.sprite.Sprite):
    """Враг 'Полицейский' (SOLID - отдельное поведение)"""

    def __init__(self, x, y, platforms, direction=1):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)  # Синий полицейский
        self.rect = self.image.get_rect(topleft=(x, y))
        self.platforms = platforms
        self.direction = direction  # Направление стрельбы
        self.velocity = pygame.math.Vector2(0, 0)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 3000  # 3 секунды между выстрелами

    def update(self):
        """Обновление состояния полицейского"""
        # Гравитация
        self.velocity.y += GRAVITY
        self.rect.y += self.velocity.y

        # Проверка коллизий с платформами
        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in collisions:
            if self.velocity.y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0

    def shoot(self):
        """Стрельба (возвращает пулю или None)"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            bullet_x = self.rect.right if self.direction == 1 else self.rect.left
            return Projectile(bullet_x, self.rect.centery, self.direction)
        return None