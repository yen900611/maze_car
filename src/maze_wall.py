import Box2D
import pygame
from .env import *


def count_position(vertices):
    v_sum = (0, 0)
    for vertice in vertices:
        v_sum += vertice
    position = v_sum[0] / 4, v_sum[1] / 4
    return position

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, vertices, world):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.world = world
        self.x, self.y = (0, 0)
        self.body = world.CreateKinematicBody(position = (0, 0))
        self.box = self.body.CreatePolygonFixture(box = ((TILESIZE/ (2*PPM), TILESIZE/ (2*PPM))), vertices = vertices)

class VerticalMoveWall(Wall):
    def __init__(self, game, vertices, world, velocity, distance=None):
        Wall.__init__(self, game, vertices, world)
        if distance > 0:
            self.start_coordinate = self.body.position[0], self.body.position[1]
            self.end_coordinate = self.body.position[0], self.body.position[1] + distance
        elif distance < 0:
            self.start_coordinate = self.body.position[0], self.body.position[1] + distance
            self.end_coordinate = self.body.position[0], self.body.position[1]
        self.velocity = abs(velocity)
        self.body.linearVelocity = (0, self.velocity)

    def update(self, *args, **kwargs) -> None:
        if self.body.position[1] > self.end_coordinate[1]:
            self.body.linearVelocity = (0, -self.velocity)
        elif self.body.position[1] < self.start_coordinate[1]:
            self.body.linearVelocity = (0, self.velocity)

class HorizontalMoveWall(Wall):
    def __init__(self, game, vertices, world, velocity, distance):
        Wall.__init__(self, game, vertices, world)
        if distance > 0:
            self.start_coordinate = self.body.position[0], self.body.position[1]
            self.end_coordinate = self.body.position[0] + distance, self.body.position[1]
        elif distance < 0:
            self.start_coordinate = self.body.position[0] + distance, self.body.position[1]
            self.end_coordinate = self.body.position[0], self.body.position[1]

        self.velocity = abs(velocity)
        self.body.linearVelocity = (self.velocity, 0)

    def update(self, *args, **kwargs) -> None:
        if self.body.position[0] > self.end_coordinate[0]:
            self.body.linearVelocity = (-self.velocity, 0)
        elif self.body.position[0] < self.start_coordinate[0]:
            self.body.linearVelocity = (self.velocity, 0)

class SlantWall(Wall):
    def __init__(self, game, vertices, world):
        Wall.__init__(self, game, vertices, world)
        self.game = game
        self.world = world
        self.x, self.y = (0, 0)
        self.body = world.CreateKinematicBody(position = (0, 0))
        self.box = self.body.CreatePolygonFixture(vertices = vertices)
        pass
