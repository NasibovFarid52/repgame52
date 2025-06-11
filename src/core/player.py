import pygame
from constants import PLAYER_SPEED, JUMP_FORCE, GRAVITY
from src.entities.projectile import Projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 255, 0))  # Зеленый прямоугольник
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True

        # Параметры стрельбы
        self.ammo = 6
        self.max_ammo = 6
        self.reload_time = 3000  # 3 секунды на перезарядку
        self.last_shot = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Движение влево/вправо
        self.velocity.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
            self.facing_right = True

    def jump(self):
        if self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.ammo > 0 and current_time - self.last_shot > 300:  # Задержка 300 мс между выстрелами
            self.ammo -= 1
            self.last_shot = current_time
            # Создаем пулю
            direction = 1 if self.facing_right else -1
            # Позиция пули: впереди игрока
            if self.facing_right:
                bullet_x = self.rect.right
            else:
                bullet_x = self.rect.left
            bullet_y = self.rect.centery
            return Projectile(bullet_x, bullet_y, direction)  # Возвращаем объект пули
        return None

    def update(self, platforms):
        self.handle_input()
        # Применяем гравитацию
        self.velocity.y += GRAVITY
        self.rect.y += self.velocity.y
        self.on_ground = False

        # Проверка коллизий с платформами по вертикали
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:  # Падаем вниз
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:  # Двигаемся вверх
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

        # Горизонтальное движение и коллизии
        self.rect.x += self.velocity.x
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:  # Движение влево
                    self.rect.left = platform.rect.right

        # Автоматическая перезарядка
        current_time = pygame.time.get_ticks()
        if self.ammo < self.max_ammo and current_time - self.last_shot > self.reload_time:
            self.ammo = self.max_ammo

    def reset(self, x, y):
        """Сброс состояния игрока при перезапуске уровня"""
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.ammo = self.max_ammo
        self.last_shot = 0
        self.on_ground = False