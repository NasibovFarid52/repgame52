import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, KEY_JUMPS, KEY_SHOOT, BACKGROUNDS_PATH
from src.core.player import Player
from src.utils.helpers import load_progress, save_progress
from src.utils.level_loader import load_level
from src.entities.rat import Rat
from src.entities.policeman import Policeman
from src.entities.disk import Disk
from src.entities.platform import Platform
from src.entities.door import Door


class GameLevel:
    def __init__(self, game, level_num):
        self.game = game
        self.level_num = level_num
        self.progress = load_progress()

        # Создаем группы заранее
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.disks = pygame.sprite.Group()
        self.player = None
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.camera_offset = pygame.math.Vector2(0, 0)
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 24)
        self.paused = False
        self.door = None
        self.door_spawned = False

        # Загрузка уровня
        self.level_data = load_level(level_num)
        if not self.level_data:
            self.game.set_scene("level_select")
            return

        # Инициализация уровня
        self.initialize_level()

        # Инициализация счетчиков ПОСЛЕ загрузки уровня
        self.total_disks = len(self.disks)

        # Загрузка фонового изображения для уровня
        self.background = None
        try:
            # Пытаемся загрузить фоновое изображение для текущего уровня
            bg_path = os.path.join(BACKGROUNDS_PATH, f"level{level_num}.png")
            self.background = pygame.image.load(bg_path)
            # Масштабируем изображение под размер экрана
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Не удалось загрузить фоновое изображение для уровня {level_num}: {e}")

    def initialize_level(self):

        # Очищаем группы
        self.platforms.empty()
        self.enemies.empty()
        self.disks.empty()
        self.all_sprites.empty()
        self.bullets.empty()

        # Создаем объекты из данных уровня
        platforms = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        disks = pygame.sprite.Group()

        # Загрузка платформ
        for plat in self.level_data["platforms"]:
            p = Platform(
                plat["x"],
                plat["y"],
                plat["width"],
                plat["height"],
                plat.get("type", "static")
            )
            platforms.add(p)

        # Загрузка врагов
        for enemy in self.level_data["enemies"]:
            if enemy["type"] == "rat":
                e = Rat(enemy["x"], enemy["y"], platforms)
            elif enemy["type"] == "policeman":
                e = Policeman(enemy["x"], enemy["y"], platforms, enemy.get("direction", 1))
            enemies.add(e)

        # Загрузка дисков
        for disk in self.level_data["disks"]:
            d = Disk(disk["x"], disk["y"])
            disks.add(d)

        # Позиция игрока
        player_start = (self.level_data["player"]["x"], self.level_data["player"]["y"])

        # Наполняем группы
        self.platforms = platforms
        self.enemies = enemies
        self.disks = disks
        self.player = Player(*player_start)

        # Сбрасываем состояние двери
        self.door = None
        self.door_spawned = False
        self.score = 0
        self.bullets.empty()

        # Добавляем объекты в группу спрайтов
        self.all_sprites.add(self.platforms, self.enemies, self.disks, self.player)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_scene("pause")
            if event.key in KEY_JUMPS:
                self.player.jump()
            if event.key == KEY_SHOOT:
                bullet = self.player.shoot()
                if bullet:  # Проверяем, что bullet - это объект Projectile
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

    def update(self):
        if self.paused:
            return

        # Обновление игрока
        self.player.update(self.platforms)

        # Список для новых пуль
        new_bullets = []

        # Обновление врагов и сбор пуль
        for enemy in self.enemies:
            if isinstance(enemy, Rat):
                enemy.update()
            elif isinstance(enemy, Policeman):
                enemy.update()

                # Получаем пулю, если она есть
                bullet = enemy.get_bullet()
                if bullet:
                    new_bullets.append(bullet)

        # Добавляем все новые пули одновременно
        for bullet in new_bullets:
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)

        # Обновление пуль
        self.bullets.update()

        # Проверка коллизий пуль с врагами
        for bullet in self.bullets:
            enemy_hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
            if enemy_hits:
                bullet.kill()
                self.score += 100

        # Проверка коллизий пуль с игроком
        player_hit = pygame.sprite.spritecollide(self.player, self.bullets, True)
        if player_hit:
            # При смерти игрока перезагружаем уровень
            self.initialize_level()
            return  # Прерываем дальнейшее обновление в этом кадре

        # Проверка коллизий игрока с врагами
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            # При смерти игрока перезагружаем уровень
            self.initialize_level()
            return  # Прерываем дальнейшее обновление в этом кадре

        # Проверка коллизий игрока с дисками
        disk_hits = pygame.sprite.spritecollide(self.player, self.disks, True)
        for _ in disk_hits:
            self.score += 50
            # Если собраны все диски - создаем дверь
            if len(self.disks) == 0 and not self.door_spawned:
                self.spawn_door()

        # Проверка коллизии с дверью
        if self.door and pygame.sprite.collide_rect(self.player, self.door):
            self.complete_level()

        # Обновление камеры
        self.camera_offset.x = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_offset.y = self.player.rect.centery - SCREEN_HEIGHT // 2

    def spawn_door(self):

        # Ищем самую правую платформу для размещения двери
        rightmost_x = 0
        for platform in self.platforms:
            if platform.rect.right > rightmost_x:
                rightmost_x = platform.rect.right

        # Размещаем дверь на правой платформе
        door_x = rightmost_x - 60  # Ширина двери 60px
        door_y = SCREEN_HEIGHT - 150

        self.door = Door(door_x, door_y)
        self.all_sprites.add(self.door)
        self.door_spawned = True

    def draw(self, screen):
        # Отрисовка фона
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BLACK)

        # Отрисовка всех спрайтов
        for sprite in self.all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - self.camera_offset.x,
                                       sprite.rect.y - self.camera_offset.y))

        # Отрисовка пуль
        for bullet in self.bullets:
            screen.blit(bullet.image, (bullet.rect.x - self.camera_offset.x,
                                       bullet.rect.y - self.camera_offset.y))

        # Отрисовка интерфейса (счет, патроны, диски)
        score_text = self.font.render(f"Очки: {self.score}", True, WHITE)
        ammo_text = self.font.render(f"Патроны: {self.player.ammo}/6", True, WHITE)
        disks_text = self.font.render(f"Диски: {self.total_disks - len(self.disks)}/{self.total_disks}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(ammo_text, (10, 40))
        screen.blit(disks_text, (10, 70))

    def complete_level(self):

        unlocked = self.progress["unlocked"]
        next_level = self.level_num + 1
        if next_level not in unlocked and next_level <= 6:
            unlocked.append(next_level)
            self.progress["unlocked"] = unlocked
            save_progress(self.progress)

        if next_level <= 6:
            self.game.set_scene("game", level_num=next_level)
        else:
            self.game.set_scene("menu")