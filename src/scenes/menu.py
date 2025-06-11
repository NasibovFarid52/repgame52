import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, BLUE, BLACK


class MenuScene:
    """Главное меню игры (KISS - простой и понятный интерфейс)"""

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 40)
        self.title_font = pygame.font.SysFont('Arial', 60)
        self.selected = 0
        self.options = ["Начать игру", "Выйти"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:  # Начать игру
                    self.game.set_scene("level_select")
                elif self.selected == 1:  # Выйти
                    self.game.quit()

    def update(self):
        # Анимация выбора (можно добавить мигание)
        pass

    def draw(self, screen):
        # Фон
        screen.fill(BLACK)

        # Заголовок
        title = self.title_font.render("ПЛАТФОРМЕР", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Опции меню
        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected else BLUE
            text = self.font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))

        # Подсказка управления
        hint = pygame.font.SysFont('Arial', 20).render(
            "Управление: Стрелки Вверх/Вниз - выбор, Enter - подтвердить",
            True, WHITE
        )
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 500))