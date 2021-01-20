import Box2D
import pygame
from .env import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, world, ):
        pygame.sprite.Sprite.__init__(self)
        # 先建立Box2D的物件，再用Box2D換算pygame座標來建立sprite(？
        pass

    def update(self, *args, **kwargs) -> None:
        pass