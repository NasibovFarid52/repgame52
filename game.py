import pygame
from src.scenes.menu import MenuScene
from src.scenes.level_select import LevelSelectScene
from src.scenes.game_level import GameLevel
from src.scenes.pause import PauseScene
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LEVEL_MUSIC, MENU_MUSIC, MUSIC_VOLUME
from src.utils.helpers import load_progress
from src.core.sound_manager import SoundManager


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BANDANA 2")
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

        pygame.mixer.init()
        self.current_music = None
        self.sound_manager = SoundManager()


    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
        self.sound_manager.set_volume(volume)


    def run(self):
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

        if scene_name in ["menu", "level_select"]:
            new_music = MENU_MUSIC
        elif scene_name == "game":
            level_num = kwargs.get("level_num", self.current_level)
            self.current_level = level_num
            if 1 <= level_num <= len(LEVEL_MUSIC):
                new_music = LEVEL_MUSIC[level_num - 1]
            else:
                new_music = MENU_MUSIC
        else:
            new_music = None

        # Меняем музыку только если это новая сцена с другим треком
        if new_music and new_music != self.current_music:
            # Плавный переход: затухание на 0,5 секунд
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load(new_music)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
            self.current_music = new_music


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
        if self.scenes.get("game"):
            level_num = self.scenes["game"].level_num
            self.set_scene("game", level_num=level_num)

    def quit(self):
        self.running = False