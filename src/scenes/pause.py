import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, BLUE, BLACK


class PauseScene:
    def __init__(self, game, game_scene):
        self.game = game
        self.game_scene = game_scene
        self.font = pygame.font.SysFont('Arial', 40)
        self.small_font = pygame.font.SysFont('Arial', 30)
        self.selected = 0
        self.options = ["Продолжить", "Начать заново", "В главное меню"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:  # Продолжить
                    self.game.set_scene("game")
                elif self.selected == 1:  # Начать заново
                    # Полностью перезагружаем текущий уровень
                    self.game_scene.initialize_level()
                    self.game.set_scene("game")
                elif self.selected == 2:  # В главное меню
                    self.game.set_scene("menu")
            elif event.key == pygame.K_ESCAPE:
                self.game.set_scene("game")

    def update(self):
        pass

    def draw(self, screen):
        # Полупрозрачный фон
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(180)
        s.fill(BLACK)
        screen.blit(s, (0, 0))

        # Панель меню
        menu_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT // 2 - 150,
            400,
            300
        )
        pygame.draw.rect(screen, (50, 50, 80), menu_rect, border_radius=15)
        pygame.draw.rect(screen, BLUE, menu_rect, 3, border_radius=15)

        # Заголовок
        title = self.font.render("ПАУЗА", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, menu_rect.y + 30))

        # Опции меню
        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected else BLUE
            text = self.font.render(option, True, color)
            screen.blit(text, (
                SCREEN_WIDTH // 2 - text.get_width() // 2,
                menu_rect.y + 100 + i * 60
            ))

        # Подсказка
        hint = self.small_font.render("Используйте стрелки для выбора и Enter для подтверждения", True, WHITE)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, menu_rect.bottom - 40))