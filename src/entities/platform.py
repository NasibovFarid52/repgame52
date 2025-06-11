import pygame
from constants import GREEN, BROWN


class Platform(pygame.sprite.Sprite):
    """Класс платформы (статичной или движущейся)"""

    def __init__(self, x, y, width, height, platform_type="static"):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if platform_type == "static":
            self.image.fill(GREEN)  # Статичная платформа - зеленая
        else:  # moving
            self.image.fill(BROWN)  # Движущаяся платформа - коричневая
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = platform_type

        # Для движущихся платформ
        self.speed = 2
        self.direction = pygame.math.Vector2(1, 0)  # Направление движения
        self.distance = 100  # Расстояние, которое проходит платформа
        self.start_x = x
        self.start_y = y

    def update(self):
        """Обновление позиции движущейся платформы"""
        if self.type == "moving":
            # Движение вперед и назад по горизонтали
            self.rect.x += self.speed * self.direction.x

            # Если платформа прошла заданное расстояние, меняем направление
            if abs(self.rect.x - self.start_x) > self.distance:
                self.direction.x *= -1