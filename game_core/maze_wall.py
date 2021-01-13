import Box2D
import pygame
from .env import *

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass

    def update(self, *args, **kwargs) -> None:
        pass