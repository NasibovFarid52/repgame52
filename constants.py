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
Anthracite_grey = (41, 50, 65)
GREY_BROWN = (94, 80, 63)
PEARL = (234, 224, 213)
CREAM_HAKI = (198, 172, 143)

# Физика
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_FORCE = -15

# Управление
KEY_JUMP = pygame.K_SPACE
KEY_SHOOT = pygame.K_k

# Пути
ASSETS_PATH = "assets/"
DATA_PATH = "data/"
LEVELS_PATH = DATA_PATH + "levels/"
PROGRESS_FILE = DATA_PATH + "progress.json"
IMAGES_PATH = ASSETS_PATH + "images/"