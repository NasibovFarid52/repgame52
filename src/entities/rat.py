import pygame
from constants import BROWN, GRAVITY


class Rat(pygame.sprite.Sprite):
    """Враг 'Крыса' (KISS - простое поведение)"""

    def __init__(self, x, y, platforms):
        super().__init__()
        self.image = pygame.Surface((30, 20))
        self.image.fill(BROWN)  # Коричневая крыса
        self.rect = self.image.get_rect(topleft=(x, y))
        self.platforms = platforms
        self.speed = 2
        self.direction = 1  # 1 - вправо, -1 - влево
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        """Обновление состояния крысы"""
        # Гравитация
        self.velocity.y += GRAVITY
        self.rect.y += self.velocity.y

        # Проверка коллизий с платформами
        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in collisions:
            if self.velocity.y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0

        # Движение по платформе
        self.rect.x += self.speed * self.direction

        # Проверка края платформы
        if not self.is_on_platform():
            self.direction *= -1  # Разворот

    def is_on_platform(self):
        """Проверка, стоит ли крыса на платформе"""
        # Смещаем rect вниз на 1 пиксель для проверки
        test_rect = self.rect.copy()
        test_rect.y += 2
        return any(platform.rect.colliderect(test_rect) for platform in self.platforms)