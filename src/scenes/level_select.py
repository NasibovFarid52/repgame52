import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, ANTHRACITE_GREY, IMAGES_PATH, GREY_BROWN, PEARL, \
    CREAM_HAKI, GREY


class LevelSelectScene:

    def __init__(self, game):
        self.game = game

        # Загрузка фонового изображения
        self.background = pygame.image.load(IMAGES_PATH + "bandana_2.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Шрифты
        self.title_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.option_font = pygame.font.SysFont('Arial', 36)
        self.hint_font = pygame.font.SysFont('Arial', 20)

        self.selected = 0
        self.levels = self.get_available_levels()

    def get_available_levels(self):
        """Получаем список доступных уровней"""
        progress = self.game.progress
        unlocked = progress["unlocked"]

        # Определяем общее количество уровней
        total_levels = 6

        # Создаем список с доступностью
        return [
            {"num": i + 1, "name": f"Уровень {i + 1}", "unlocked": (i + 1) in unlocked}
            for i in range(total_levels)
        ]

    def create_button_textures(self):
        """Создает текстуры для кнопок уровней"""
        textures = []
        for i, level in enumerate(self.levels):
            # Создаем поверхность для кнопки
            button = pygame.Surface((300, 60), pygame.SRCALPHA)

            # Основной цвет кнопки
            main_color = ANTHRACITE_GREY

            # Отрисовываем кнопку
            pygame.draw.rect(button, main_color, (0, 0, 300, 60), border_radius=15)

            # Рамка
            border_color = BLACK
            pygame.draw.rect(button, border_color, (0, 0, 300, 60), 2, border_radius=15)

            # Текст кнопки
            if level["unlocked"]:
                text_color = PEARL if i != self.selected else GREY_BROWN
                text = self.option_font.render(level["name"], True, text_color)
            else:
                text_color = GREY  # Серый для заблокированных
                text = self.option_font.render("Заблокировано", True, text_color)

            button.blit(text, (150 - text.get_width() // 2, 30 - text.get_height() // 2))

            textures.append(button)
        return textures

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Пропускаем заблокированные уровни при навигации
                new_selected = self.selected
                while True:
                    new_selected = (new_selected - 1) % len(self.levels)
                    if self.levels[new_selected]["unlocked"] or new_selected == self.selected:
                        break
                self.selected = new_selected
            elif event.key == pygame.K_DOWN:
                # Пропускаем заблокированные уровни при навигации
                new_selected = self.selected
                while True:
                    new_selected = (new_selected + 1) % len(self.levels)
                    if self.levels[new_selected]["unlocked"] or new_selected == self.selected:
                        break
                self.selected = new_selected
            elif event.key == pygame.K_RETURN:
                # Загружаем уровень только если он разблокирован
                if self.levels[self.selected]["unlocked"]:
                    self.game.set_scene("game", level_num=self.levels[self.selected]["num"])
            elif event.key == pygame.K_ESCAPE:
                self.game.set_scene("menu")

    def update(self):
        pass

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.background, (0, 0))

        # Эффект затемнения фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Полупрозрачный черный
        screen.blit(overlay, (0, 0))

        # Создаем текстуры кнопок
        button_textures = self.create_button_textures()

        # Заголовок
        title = self.title_font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, CREAM_HAKI)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Отрисовка кнопок уровней
        for i, texture in enumerate(button_textures):
            y_pos = 130 + i * 70
            screen.blit(texture, (SCREEN_WIDTH // 2 - 150, y_pos))

        # Подсказка
        hint = self.hint_font.render(
            "Esc: Назад, Enter: Выбрать",
            True, (180, 180, 180)
        )
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))