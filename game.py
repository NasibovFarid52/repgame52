import pygame
from src.scenes.menu import MenuScene
from src.scenes.level_select import LevelSelectScene
from src.scenes.game_level import GameLevel
from src.scenes.pause import PauseScene
from src.scenes.intro_scene import IntroScene
from src.scenes.final_scene import FinalScene
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MENU_MUSIC, LEVEL_MUSIC, BLACK, MUSIC_VOLUME, MUSIC_FADEOUT
from src.core.sound_manager import SoundManager
from src.utils.helpers import load_progress


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BANDANA 2")
        self.clock = pygame.time.Clock()
        self.running = True
        self.progress = load_progress()
        self.current_level = 1

        # Звук
        pygame.mixer.init()
        self.current_music = None
        self.volume = self.progress.get("volume", MUSIC_VOLUME)
        self.sound_manager = SoundManager()
        self.sound_manager.set_volume(self.volume)

        # Инициализация сцен
        self.scenes = {
            "intro": IntroScene(self),
            "menu": MenuScene(self),
            "level_select": LevelSelectScene(self),
            "game": None,
            "pause": None,
            "final": FinalScene(self)
        }
        self.current_scene = "intro"

        # Запускаем музыку для вступительной сцены
        self.play_music(MENU_MUSIC)

    def play_music(self, music_file):
        # Плавное затухание текущей музыки
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(MUSIC_FADEOUT)
        # Загрузка и воспроизведение новой музыки
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)
        self.current_music = music_file


    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
        self.sound_manager.set_volume(volume)

        # Сохраняем громкость в прогресс
        self.progress["volume"] = volume
        from src.utils.helpers import save_progress
        save_progress(self.progress)

    def set_scene(self, scene_name, **kwargs):
        # Определяем музыку для новой сцены
        if scene_name in ["intro", "menu", "level_select"]:
            new_music = MENU_MUSIC
        elif scene_name == "game":
            level_num = kwargs.get("level_num", self.current_level)
            self.current_level = level_num
            if 1 <= level_num <= len(LEVEL_MUSIC):
                new_music = LEVEL_MUSIC[level_num - 1]
            else:
                new_music = MENU_MUSIC
        elif scene_name == "final":
            new_music = MENU_MUSIC
        else:
            new_music = None

        # Меняем музыку только если она отличается от текущей
        if new_music and new_music != self.current_music:
            self.play_music(new_music)

        # Обработка конкретных сцен
        if scene_name == "game":
            level_num = kwargs.get("level_num", self.current_level)
            self.current_level = level_num
            self.scenes["game"] = GameLevel(self, level_num)

            # Для последнего уровня устанавливаем колбэк на финальную сцену
            if level_num == 6:
                self.scenes["game"].on_complete = lambda: self.set_scene("final")
            self.current_scene = "game"


        elif scene_name == "pause":
            # При паузе передаем текущую игровую сцену
            if self.scenes.get("game"):
                self.scenes["pause"] = PauseScene(self, self.scenes["game"])
                self.current_scene = "pause"

        elif scene_name == "final":
            self.current_scene = "final"

        else:
            # Для остальных сцен просто переключаемся
            self.current_scene = scene_name

    def restart_level(self):
        if self.scenes.get("game"):
            level_num = self.scenes["game"].level_num
            self.set_scene("game", level_num=level_num)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Передаем событие текущей сцене
                if self.current_scene and self.scenes.get(self.current_scene):
                    self.scenes[self.current_scene].handle_event(event)

            # Обновление текущей сцены
            if self.current_scene and self.scenes.get(self.current_scene):
                self.scenes[self.current_scene].update()

            # Отрисовка
            self.screen.fill((BLACK))
            if self.current_scene and self.scenes.get(self.current_scene):
                self.scenes[self.current_scene].draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)