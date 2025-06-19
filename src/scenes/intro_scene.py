import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_PATH, PURPLE, YELLOW


class IntroScene:
    def __init__(self, game):
        self.game = game
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.background = pygame.image.load(IMAGES_PATH + "letter_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.set_scene("menu")

    def update(self):
        pass

    def draw(self, screen):
        # Отрисовка фона
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((YELLOW))

        # Подсказка
        hint = self.small_font.render("Нажмите ENTER, чтобы вернуться в меню", True, (PURPLE))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))