import pygame
import os
from constants import PLATFORMS_PATH


class Platform(pygame.sprite.Sprite):

    # Загружаем текстуры платформ один раз при инициализации класса
    _textures_loaded = False
    _static_texture = None

    @classmethod
    def load_textures(cls):
        if not cls._textures_loaded:
                # Загружаем текстуру для статичной платформы
                cls._static_texture = pygame.image.load(os.path.join(PLATFORMS_PATH, "platform_static.png"))
                cls._textures_loaded = True


    def __init__(self, x, y, width, height, platform_type="static"):
        super().__init__()

        # Загружаем текстуры при первом создании платформы
        if not Platform._textures_loaded:
            Platform.load_textures()

        self.type = platform_type
        self.width = width
        self.height = height

        # Создаем поверхность для платформы
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # Выбираем текстуру
        texture = Platform._static_texture

        # Заполняем поверхность плитками
        tile_size = texture.get_size()[0]
        for i in range(0, width, tile_size):
            for j in range(0, height, tile_size):
                # Определяем размер последней плитки
                tile_width = min(tile_size, width - i)
                tile_height = min(tile_size, height - j)

                if tile_width < tile_size or tile_height < tile_size:
                    # Если это неполная плитка, создаем фрагмент текстуры
                    tile = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                    tile.blit(texture, (0, 0), (0, 0, tile_width, tile_height))
                    self.image.blit(tile, (i, j))
                else:
                    # Полная плитка
                    self.image.blit(texture, (i, j))
        self.rect = self.image.get_rect(topleft=(x, y))


    def update(self):
        pass