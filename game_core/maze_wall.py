import Box2D
import pygame
from .env import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, world, vertices, size):
        pygame.sprite.Sprite.__init__(self)
        # 先建立Box2D的物件，再用Box2D換算pygame座標來建立sprite(？
        self.body = world.CreateKinematicBody(position=(0, 0), linearVelocity=(0, 0))
        box = self.body.CreatePolygonFixture(vertices=vertices)
        pass

    def update(self) -> None:
        pass
