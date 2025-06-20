import pygame
import os
from constants import GRAVITY, ENEMIES_PATH, POLICEMAN_SHOOT_DELAY, ENEMY_ANIMATION_SPEED
from src.entities.projectile import Projectile


class Policeman(pygame.sprite.Sprite):


    # Загружаем текстуры один раз при инициализации класса
    _textures_loaded = False
    _idle_texture = None
    _shoot_texture = None

    @classmethod
    def load_textures(cls):
        if not cls._textures_loaded:
            # Загружаем только 2 кадра: стойка и стрельба
            cls._idle_texture = pygame.image.load(os.path.join(ENEMIES_PATH, "policeman_idle.png"))
            cls._shoot_texture = pygame.image.load(os.path.join(ENEMIES_PATH, "policeman_shoot.png"))
            # Масштабируем до стандартного размера
            size = (60, 80)
            cls._idle_texture = pygame.transform.scale(cls._idle_texture, size)
            cls._shoot_texture = pygame.transform.scale(cls._shoot_texture, size)
            cls._textures_loaded = True


    def __init__(self, x, y, platforms, direction=1):
        super().__init__()

        # Загружаем текстуры при первом создании полицейского
        if not Policeman._textures_loaded:
            Policeman.load_textures()

        self.platforms = platforms
        self.direction = direction
        self.velocity = pygame.math.Vector2(0, 0)

        # Начальное состояние
        self.state = "idle"
        self.image = Policeman._idle_texture
        if direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Таймеры для стрельбы
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = POLICEMAN_SHOOT_DELAY
        self.is_shooting = False
        self.shoot_start_time = 0
        self.bullet_to_spawn = None

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

        # Текущее время
        current_time = pygame.time.get_ticks()

        # Логика стрельбы
        if self.state == "idle":
            # Проверяем, можно ли стрелять
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.state = "shooting"
                self.shoot_start_time = current_time
                self.is_shooting = True

                # Сразу меняем текстуру на стрельбу
                self.image = Policeman._shoot_texture
                if self.direction < 0:
                    self.image = pygame.transform.flip(self.image, True, False)

                # Создаем пулю
                self.spawn_bullet()

        elif self.state == "shooting":
            # Проверяем, закончилась ли анимация стрельбы
            if current_time - self.shoot_start_time > ENEMY_ANIMATION_SPEED:
                self.state = "idle"
                self.last_shot_time = current_time
                self.is_shooting = False

                # Возвращаем текстуру стойки
                self.image = Policeman._idle_texture
                if self.direction < 0:
                    self.image = pygame.transform.flip(self.image, True, False)

    def spawn_bullet(self):

        # Определяем позицию вылета пули
        if self.direction > 0:
            bullet_x = self.rect.right
        else:
            bullet_x = self.rect.left

        bullet_y = self.rect.top

        # Создаем пулю
        self.bullet_to_spawn = (bullet_x, bullet_y, self.direction)

    def get_bullet(self):

        if self.bullet_to_spawn:
            bullet = Projectile(*self.bullet_to_spawn)
            self.bullet_to_spawn = None
            return bullet
        return None