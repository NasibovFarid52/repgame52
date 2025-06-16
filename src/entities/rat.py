import pygame
import os
from constants import GRAVITY, BROWN, ENEMIES_PATH


class Rat(pygame.sprite.Sprite):
    """Враг 'Крыса' с анимацией"""

    # Загружаем текстуры один раз при инициализации класса
    _textures_loaded = False
    _rat_textures_left = []
    _rat_textures_right = []

    @classmethod
    def load_textures(cls):
        """Загружает текстуры крысы из файлов"""
        if not cls._textures_loaded:
            try:
                # Загружаем 3 кадра анимации для движения вправо
                for i in range(1, 4):
                    texture = pygame.image.load(os.path.join(ENEMIES_PATH, f"rat{i}.png"))
                    # Масштабируем до стандартного размера
                    texture = pygame.transform.scale(texture, (40, 30))
                    cls._rat_textures_right.append(texture)

                # Создаем зеркальные текстуры для движения влево
                for texture in cls._rat_textures_right:
                    flipped = pygame.transform.flip(texture, True, False)
                    cls._rat_textures_left.append(flipped)

                cls._textures_loaded = True
            except Exception as e:
                print(f"Ошибка загрузки текстур крысы: {e}")
                # Создаем простые текстуры, если загрузка не удалась
                cls._rat_textures_right = []
                cls._rat_textures_left = []
                for i in range(3):
                    surface = pygame.Surface((30, 20))
                    surface.fill(BROWN)
                    cls._rat_textures_right.append(surface)
                    cls._rat_textures_left.append(surface)

    def __init__(self, x, y, platforms):
        super().__init__()

        # Загружаем текстуры при первом создании крысы
        if not Rat._textures_loaded:
            Rat.load_textures()

        self.platforms = platforms
        self.speed = 2
        self.direction = 1  # 1 - вправо, -1 - влево
        self.velocity = pygame.math.Vector2(0, 0)

        # Анимационные параметры
        self.textures_right = Rat._rat_textures_right
        self.textures_left = Rat._rat_textures_left
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.textures_right[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Для плавной анимации
        self.animation_counter = 0

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

        # Обновление анимации
        self.animation_counter += self.animation_speed
        if self.animation_counter >= len(self.textures_right):
            self.animation_counter = 0

        self.current_frame = int(self.animation_counter)

        # Выбор текстуры в зависимости от направления
        if self.direction > 0:
            self.image = self.textures_right[self.current_frame]
        else:
            self.image = self.textures_left[self.current_frame]

    def is_on_platform(self):
        """Проверка, стоит ли крыса на платформе"""
        # Смещаем rect вниз на 1 пиксель для проверки
        test_rect = self.rect.copy()
        test_rect.y += 2
        return any(platform.rect.colliderect(test_rect) for platform in self.platforms)