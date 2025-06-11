import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, BLUE, BLACK


class PauseScene:
    def __init__(self, game, game_scene):
        self.game = game
        self.game_scene = game_scene
        self.font = pygame.font.SysFont('Arial', 40)
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
                    self.game.restart_level()
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

        # Заголовок
        title = self.font.render("ПАУЗА", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        # Опции меню
        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected else BLUE
            text = self.font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))