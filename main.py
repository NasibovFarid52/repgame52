import pygame
from src.core.game import Game

def main():
    pygame.init()
    pygame.mixer.init()
    game = Game()
    game.run()

if __name__ == "__main__":
    main()