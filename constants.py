import pygame

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
GREY = (100, 100, 100)
ANTHRACITE_GREY = (41, 50, 65)
GREY_BROWN = (94, 80, 63)
PEARL = (234, 224, 213)
CREAM_HAKI = (198, 172, 143)

# Физика
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_FORCE = -15
ENEMY_ANIMATION_SPEED = 0.2
POLICEMAN_SHOOT_DELAY = 1000
PLAYER_ANIMATION_SPEED = 0.15

# Управление
KEY_JUMPS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
KEY_SHOOT = pygame.K_k

# Пути
ASSETS_PATH = "assets/"
DATA_PATH = "data/"
LEVELS_PATH = DATA_PATH + "levels/"
PROGRESS_FILE = DATA_PATH + "progress.json"
IMAGES_PATH = ASSETS_PATH + "images/"
BACKGROUNDS_PATH = IMAGES_PATH + "backgrounds/"
PLATFORMS_PATH = IMAGES_PATH + "platforms/"
COLLECTIBLES_PATH = IMAGES_PATH + "collectibles/"
DOORS_PATH = IMAGES_PATH + "doors/"
ENEMIES_PATH = IMAGES_PATH + "enemies/"
PROJECTILES_PATH = IMAGES_PATH + "projectiles/"
PLAYER_PATH = IMAGES_PATH + "player/"

# Музыка
MUSIC_VOLUME = 0.03
MUSIC_PATH = ASSETS_PATH + "music/"
MENU_MUSIC = MUSIC_PATH + "menu_music.mp3"
LEVEL_MUSIC = [
    MUSIC_PATH + "level1_music.mp3",
    MUSIC_PATH + "level2_music.mp3",
    MUSIC_PATH + "level3_music.mp3",
    MUSIC_PATH + "level4_music.mp3",
    MUSIC_PATH + "level5_music.mp3",
    MUSIC_PATH + "level6_music.mp3"
]

# Звуковые эффекты
SOUNDS_PATH = ASSETS_PATH + "sounds/"
SHOOT_SOUND = SOUNDS_PATH + "shoot.wav"
RAT_DEATH_SOUND = SOUNDS_PATH + "rat_death.wav"
POLICEMAN_DEATH_SOUND = SOUNDS_PATH + "policeman_death.wav"
DOOR_ENTER_SOUND = SOUNDS_PATH + "door_enter.wav"