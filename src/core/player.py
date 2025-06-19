import pygame
import os
from constants import PLAYER_SPEED, JUMP_FORCE, GRAVITY, PLAYER_ANIMATION_SPEED, PLAYER_PATH
from src.entities.projectile import Projectile


class Player(pygame.sprite.Sprite):


    # Загружаем текстуры один раз при инициализации класса
    _textures_loaded = False
    _idle_textures = []
    _run_textures = []
    _jump_textures = []

    @classmethod
    def load_textures(cls):

        if not cls._textures_loaded:
            try:
                # Загружаем текстуры для анимации покоя
                idle_frame = pygame.image.load(os.path.join(PLAYER_PATH, "idle.png"))
                cls._idle_textures = [pygame.transform.scale(idle_frame, (50, 60))]

                # Загружаем текстуры для бега
                cls._run_textures = []
                for i in range(1, 4):
                    frame = pygame.image.load(os.path.join(PLAYER_PATH, f"run_{i}.png"))
                    cls._run_textures.append(pygame.transform.scale(frame, (50, 60)))

                # Загружаем текстуры для прыжка
                cls._jump_textures = []
                for i in range(1, 4):
                    frame = pygame.image.load(os.path.join(PLAYER_PATH, f"jump_{i}.png"))
                    cls._jump_textures.append(pygame.transform.scale(frame, (50, 60)))

                cls._textures_loaded = True
            except Exception as e:
                print(f"Ошибка загрузки текстур игрока: {e}")

                cls._idle_textures = [pygame.Surface((40, 60))]
                cls._idle_textures[0].fill((0, 255, 0))

                cls._run_textures = []
                for i in range(3):
                    surface = pygame.Surface((40, 60))
                    surface.fill((0, 200 + i * 20, 0))
                    cls._run_textures.append(surface)

                cls._jump_textures = []
                for i in range(3):
                    surface = pygame.Surface((40, 60))
                    surface.fill((0, 150, i * 30))
                    cls._jump_textures.append(surface)

    def __init__(self, x, y):
        super().__init__()

        # Загружаем текстуры при первом создании игрока
        if not Player._textures_loaded:
            Player.load_textures()

        # Начальное состояние
        self.state = "idle"
        self.facing_right = True
        self.image = Player._idle_textures[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Анимационные параметры
        self.animation_frame = 0
        self.animation_timer = 0

        # Физические параметры
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

        # Параметры стрельбы
        self.ammo = 6
        self.max_ammo = 6
        self.reload_time = 1500
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
            # Начинаем анимацию прыжка
            self.state = "jump"
            self.animation_frame = 0
            self.animation_timer = 0

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.ammo > 0 and current_time - self.last_shot > 300:
            self.ammo -= 1
            self.last_shot = current_time

            # Создаем пулю с отступом от игрока
            direction = 1 if self.facing_right else -1
            offset = 25  # Отступ, чтобы пуля не появлялась внутри игрока

            if self.facing_right:
                bullet_x = self.rect.right + offset
            else:
                bullet_x = self.rect.left - offset

            bullet_y = self.rect.centery

            return Projectile(bullet_x, bullet_y, direction)
        return None

    def update_animation(self):

        self.animation_timer += PLAYER_ANIMATION_SPEED

        # Обработка состояния "прыжок"
        if self.state == "jump":
            # Прыжок не зациклен, показываем все 3 кадра последовательно
            if self.animation_frame < len(Player._jump_textures) - 1:
                if self.animation_timer >= 1:
                    self.animation_frame += 1
                    self.animation_timer = 0
            # Если игрок приземлился, переключаемся на idle или run
            if self.on_ground and self.animation_frame == len(Player._jump_textures) - 1:
                self.state = "idle" if self.velocity.x == 0 else "run"
                self.animation_frame = 0

        # Обработка состояния "бег"
        elif self.state == "run":
            if self.animation_timer >= 1:
                self.animation_frame = (self.animation_frame + 1) % len(Player._run_textures)
                self.animation_timer = 0

        # Обработка состояния "покой"
        elif self.state == "idle":
            self.animation_frame = 0

        # Выбор текстуры в зависимости от состояния и кадра
        if self.state == "idle":
            texture = Player._idle_textures[0]
        elif self.state == "run":
            texture = Player._run_textures[self.animation_frame]
        elif self.state == "jump":
            texture = Player._jump_textures[self.animation_frame]

        # Отражаем текстуру, если смотрит влево
        if not self.facing_right:
            texture = pygame.transform.flip(texture, True, False)

        self.image = texture

    def update(self, platforms):
        self.handle_input()

        # Обновление состояния
        if self.on_ground:
            if self.velocity.x != 0:
                self.state = "run"
            else:
                self.state = "idle"

        # Обновление анимации
        self.update_animation()

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
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.ammo = self.max_ammo
        self.last_shot = 0
        self.on_ground = False
        self.state = "idle"
        self.animation_frame = 0
        self.animation_timer = 0