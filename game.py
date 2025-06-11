import pygame
from src.scenes.menu import MenuScene
from src.scenes.level_select import LevelSelectScene
from src.scenes.game_level import GameLevel
from src.scenes.pause import PauseScene
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.utils.helpers import load_progress


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Платформер")
        self.clock = pygame.time.Clock()
        self.running = True
        self.progress = load_progress()
        self.current_level = 1  # Добавляем отслеживание текущего уровня

        # Инициализация сцен
        self.scenes = {
            "menu": MenuScene(self),
            "level_select": LevelSelectScene(self),
            "game": None,  # Будет создаваться при загрузке уровня
            "pause": None  # Будет создаваться при паузе
        }
        self.current_scene = "menu"

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Передаем событие текущей сцене
                if self.current_scene and self.scenes[self.current_scene]:
                    self.scenes[self.current_scene].handle_event(event)

            # Обновление текущей сцены
            if self.current_scene and self.scenes[self.current_scene]:
                self.scenes[self.current_scene].update()

            # Отрисовка
            self.screen.fill((0, 0, 0))  # Черный фон
            if self.current_scene and self.scenes[self.current_scene]:
                self.scenes[self.current_scene].draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def set_scene(self, scene_name, **kwargs):
        """Переключает сцену"""
        if scene_name == "game":
            level_num = kwargs.get("level_num", self.current_level)
            self.current_level = level_num  # Сохраняем текущий уровень

            # Если игра уже запущена для этого уровня, просто продолжаем
            if self.scenes.get("game") and self.scenes["game"].level_num == level_num:
                self.current_scene = "game"
            else:
                # Создаем новую игровую сцену
                try:
                    self.scenes["game"] = GameLevel(self, level_num)
                    self.current_scene = "game"
                except Exception as e:
                    print(f"Ошибка загрузки уровня: {e}")
                    self.set_scene("level_select")

        elif scene_name == "pause":
            # При паузе передаем текущую игровую сцену
            self.scenes["pause"] = PauseScene(self, self.scenes["game"])
            self.current_scene = "pause"
        else:
            self.current_scene = scene_name

    def restart_level(self):
        """Перезапускает текущий уровень"""
        if self.scenes.get("game"):
            level_num = self.scenes["game"].level_num
            self.set_scene("game", level_num=level_num)

    def quit(self):
        """Выход из игры"""
        self.running = False