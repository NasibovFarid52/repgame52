import pygame
import os
from constants import PROJECTILES_PATH, SCREEN_WIDTH


class Projectile(pygame.sprite.Sprite):

    # Загружаем текстуры один раз при инициализации класса
    _textures_loaded = False
    _bullet_texture = None

    @classmethod
    def load_texture(cls):
        """Загружает текстуру пули из файла"""
        if not cls._textures_loaded:
            try:
                # Загружаем текстуру пули
                cls._bullet_texture = pygame.image.load(os.path.join(PROJECTILES_PATH, "bullet.png"))

                # Масштабируем до нужного размера
                width, height = 13, 7
                cls._bullet_texture = pygame.transform.scale(cls._bullet_texture, (width, height))

                cls._textures_loaded = True
            except Exception as e:
                print(f"Ошибка загрузки текстуры пули: {e}")
                # Создаем простую пулю, если текстура не загружена
                cls._bullet_texture = pygame.Surface((20, 10))
                cls._bullet_texture.fill((255, 0, 0))  # Красный прямоугольник

    def __init__(self, x, y, direction):
        super().__init__()

        # Загружаем текстуру при первом создании пули
        if not Projectile._textures_loaded:
            Projectile.load_texture()

        self.image = Projectile._bullet_texture

        # Если пуля летит влево, отражаем изображение
        if direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.x += self.speed * self.direction

        # Удаление пули при выходе за пределы экрана
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()