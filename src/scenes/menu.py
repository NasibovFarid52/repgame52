import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, BLUE, BLACK, Anthracite_grey, IMAGES_PATH, GREY_BROWN, \
    PEARL, CREAM_HAKI


class MenuScene:
    """Главное меню игры с новым дизайном в стиле банданы"""

    def __init__(self, game):
        self.game = game

        # Загрузка фонового изображения
        self.background = pygame.image.load(IMAGES_PATH + "bandana_2.png")

        # Масштабируем изображение под размер экрана
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Шрифты
        self.title_font = pygame.font.SysFont('Arial', 80, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 40, italic=True)
        self.option_font = pygame.font.SysFont('Arial', 36)
        self.hint_font = pygame.font.SysFont('Arial', 20)

        self.selected = 0
        self.options = ["НАЧАТЬ ИГРУ", "ВЫЙТИ"]

        # Создаем текстуры для кнопок
        self.button_textures = self.create_button_textures()

        # Анимационные переменные
        self.title_glow = 0
        self.glow_direction = 1

    def create_button_textures(self):
        """Создает текстуры для кнопок с эффектом банданы"""
        textures = []
        for i, option in enumerate(self.options):
            # Создаем поверхность для кнопки
            button = pygame.Surface((400, 70), pygame.SRCALPHA)

            # Основной цвет кнопки
            main_color = Anthracite_grey

            # Отрисовываем кнопку
            pygame.draw.rect(button, main_color, (0, 0, 400, 70), border_radius=20)

            # Черная рамка
            pygame.draw.rect(button, BLACK, (0, 0, 400, 70), 2, border_radius=20)

            # Текст кнопки
            text_color = GREY_BROWN if i == self.selected else PEARL
            text = self.option_font.render(option, True, text_color)
            button.blit(text, (200 - text.get_width() // 2, 35 - text.get_height() // 2))

            textures.append(button)
        return textures

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                self.button_textures = self.create_button_textures()  # Обновляем текстуры
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                self.button_textures = self.create_button_textures()  # Обновляем текстуры
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:  # Начать игру
                    self.game.set_scene("level_select")
                elif self.selected == 1:  # Выйти
                    self.game.quit()

    def update(self):
        # Анимация свечения заголовка
        self.title_glow += 0.05 * self.glow_direction
        if self.title_glow > 1:
            self.title_glow = 1
            self.glow_direction = -1
        elif self.title_glow < 0:
            self.title_glow = 0
            self.glow_direction = 1

    def draw(self, screen):
        # Отрисовка фона
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BLACK)

        # Эффект затемнения фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Полупрозрачный черный
        screen.blit(overlay, (0, 0))

        # Цвета заголовка
        title_color = CREAM_HAKI
        glow_color = GREY_BROWN

        # Отрисовка объёмности букв
        title = self.title_font.render("BANDANA 2", True, glow_color)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 3, 100 + 3))

        # Основной заголовок
        title = self.title_font.render("BANDANA 2", True, title_color)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))


        # Отрисовка кнопок
        for i, texture in enumerate(self.button_textures):
            y_pos = 300 + i * 100
            screen.blit(texture, (SCREEN_WIDTH // 2 - 200, y_pos))


        # Подсказка управления
        hint = self.hint_font.render("Управление: Стрелки Вверх/Вниз - выбор, Enter - подтвердить", True,
                                     (180, 180, 180))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))