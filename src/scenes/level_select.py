import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, BLUE, BLACK, LEVELS_PATH
from src.utils.helpers import load_progress


class LevelSelectScene:
    """Выбор уровня (SOLID - отдельная ответственность)"""

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 40)
        self.title_font = pygame.font.SysFont('Arial', 50)
        self.selected = 0
        self.levels = self.get_available_levels()

    def get_available_levels(self):
        """Получаем список доступных уровней"""
        progress = load_progress()
        unlocked = progress["unlocked"]

        # Определяем общее количество уровней
        total_levels = 6

        # Создаем список с доступностью
        return [
            {"num": i + 1, "name": f"Уровень {i + 1}", "unlocked": (i + 1) in unlocked}
            for i in range(total_levels)
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.levels)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.levels)
            elif event.key == pygame.K_RETURN:
                # Загружаем уровень только если он разблокирован
                if self.levels[self.selected]["unlocked"]:
                    self.game.set_scene("game", level_num=self.levels[self.selected]["num"])
            elif event.key == pygame.K_ESCAPE:
                self.game.set_scene("menu")

    def update(self):
        # Можно добавить анимацию
        pass

    def draw(self, screen):
        screen.fill(BLACK)

        # Заголовок
        title = self.title_font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Список уровней
        for i, level in enumerate(self.levels):
            color = GREEN if level["unlocked"] else (100, 100, 100)  # Серый для заблокированных
            if i == self.selected:
                # Выделение выбранного уровня
                pygame.draw.rect(screen, BLUE, (
                    SCREEN_WIDTH // 2 - 150,
                    150 + i * 60,
                    300,
                    50
                ), 2)

            text = self.font.render(level["name"], True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 160 + i * 60))

        # Подсказка
        hint = pygame.font.SysFont('Arial', 20).render(
            "Esc: Назад, Enter: Выбрать",
            True, WHITE
        )
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))