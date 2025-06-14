import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, ANTHRACITE_GREY, IMAGES_PATH, GREY_BROWN, PEARL, CREAM_HAKI


class PauseScene:

    def __init__(self, game, game_scene):
        self.game = game
        self.game_scene = game_scene

        # Загрузка фонового изображения
        self.background = pygame.image.load(IMAGES_PATH + "bandana_2.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Шрифты
        self.title_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.option_font = pygame.font.SysFont('Arial', 36)
        self.hint_font = pygame.font.SysFont('Arial', 20)

        self.selected = 0
        self.options = ["Продолжить", "Начать заново", "В главное меню"]

        # Создаем текстуры для кнопок
        self.button_textures = self.create_button_textures()

    def create_button_textures(self):
        """Создает текстуры для кнопок в стиле bandana"""
        textures = []
        for i, option in enumerate(self.options):
            # Создаем поверхность для кнопки
            button = pygame.Surface((400, 60), pygame.SRCALPHA)

            # Основной цвет кнопки
            main_color = ANTHRACITE_GREY

            # Отрисовываем кнопку
            pygame.draw.rect(button, main_color, (0, 0, 400, 60), border_radius=15)

            # Черная рамка
            pygame.draw.rect(button, BLACK, (0, 0, 400, 60), 2, border_radius=15)

            # Текст кнопки
            text_color = GREY_BROWN if i == self.selected else PEARL
            text = self.option_font.render(option, True, text_color)
            button.blit(text, (200 - text.get_width() // 2, 30 - text.get_height() // 2))

            textures.append(button)
        return textures

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                self.button_textures = self.create_button_textures()
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                self.button_textures = self.create_button_textures()
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
        # Отрисовка фона
        screen.blit(self.background, (0, 0))

        # Эффект затемнения фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Полупрозрачный черный
        screen.blit(overlay, (0, 0))

        # Панель меню
        menu_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 250,
            SCREEN_HEIGHT // 2 - 150,
            500,
            300
        )

        # Заголовок
        title = self.title_font.render("ПАУЗА", True, CREAM_HAKI)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, menu_rect.y + 30))

        # Отрисовка кнопок
        for i, texture in enumerate(self.button_textures):
            y_pos = menu_rect.y + 100 + i * 70
            screen.blit(texture, (SCREEN_WIDTH // 2 - 200, y_pos))

        # Подсказка
        hint = self.hint_font.render(
            "Используйте стрелки для выбора и Enter для подтверждения",
            True, (180, 180, 180)
        )
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, menu_rect.bottom + 110))