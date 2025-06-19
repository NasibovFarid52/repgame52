import pygame
import os
from constants import GRAVITY, ENEMIES_PATH


class Rat(pygame.sprite.Sprite):


    # Загружаем текстуры один раз при инициализации класса
    _textures_loaded = False
    _rat_textures_left = []
    _rat_textures_right = []

    @classmethod
    def load_textures(cls):
        if not cls._textures_loaded:
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


    def is_on_platform(self):

        # Создаем небольшой прямоугольник под ногами крысы
        foot_width = 10
        foot_rect = pygame.Rect(
            self.rect.centerx - foot_width // 2,
            self.rect.bottom,
            foot_width,
            2
        )

        # Проверяем, пересекается ли эта область с любой платформой
        for platform in self.platforms:
            if foot_rect.colliderect(platform.rect):
                return True

        return False

    def update(self):

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

        # Проверка края платформы с учетом ног
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