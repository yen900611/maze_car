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
    def __init__(self, game, coordinate, world, map_length):
        pygame.sprite.Sprite.__init__(self, game.walls)
        self.game = game
        self.world = world
        # self.image = pygame.Surface((TILESIZE, TILESIZE))
        # self.image.fill(WHITE)
        # self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = self.x * TILESIZE, self.y * TILESIZE
        self.x, self.y = coordinate
        self.body = world.CreateKinematicBody(position=(self.x + TILESIZE/ (2*PPM), GRIDHEIGHT + TILE_LEFTTOP[1] / PPM - self.y - TILESIZE/ (2*PPM)))
        # self.body = world.CreateKinematicBody(position=(2,2))
        self.box = self.body.CreatePolygonFixture(box = ((TILESIZE/ (2*PPM), TILESIZE/ (2*PPM))))

class Move_Wall(pygame.sprite.Sprite):
    def __init__(self, world, vertices_init, size, is_move=False, vertices_end=None, velocity=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        # 先建立Box2D的物件，再用Box2D換算pygame座標來建立sprite(？
        self.body = world.CreateKinematicBody(position=(0, 0), linearVelocity=velocity)
        self.box = self.body.CreatePolygonFixture(vertices=vertices_init)
        self.maze_size = size
        self.wall_info = []
        self.pixel_vertices = None
        self.vertices = self.box.shape.vertices
        self.is_move = is_move
        self.vertices_end = vertices_end
        self.velocity = velocity
        self.position = self.count_position(self.vertices)
        self.init_position = self.position
        if vertices_end == None:
            self.end_position = self.count_position(vertices_init)
        else:
            self.end_position = self.count_position(vertices_end)
        pass

    def update(self) -> None:
        self.get_polygon_vertice()
        self.get_wall_infomation()
        if self.is_move:
            self.move()
        pass

    def count_position(self, vertices):
        self.get_wall_infomation()
        v_sum = [0, 0]
        for vertice in vertices:
            v_sum[0] += vertice[0]
            v_sum[1] += vertice[1]
        return v_sum[0] / 4, v_sum[1] / 4

    def move(self):
        if self.end_position[1] == self.init_position[1]:
            # y軸不變，左右移動
            if self.body.linearVelocity[0] < 0:
                if self.body.position[0] < self.end_position[0] - self.init_position[0]:
                    self.body.linearVelocity[0] = self.velocity[0] * -1
            elif self.body.linearVelocity[0] > 0:
                if self.body.position[0] > 0:
                    self.body.linearVelocity[0] = self.velocity[0]
            else:
                pass
        elif self.end_position[0] == self.init_position[0]:
            # x軸不變，上下移動
            if self.velocity[1] < 0:
                #初始向下移動
                if self.body.linearVelocity[1] < 0:
                    #向下移動
                    if self.body.position[1] < self.end_position[1] - self.init_position[1]:
                        self.body.linearVelocity[1] = self.velocity[1] * -1
                elif self.body.linearVelocity[1] > 0:
                    if self.body.position[1] > 0:
                        self.body.linearVelocity[1] = self.velocity[1]
                else:
                    pass
            elif self.velocity[1] > 0:
                #初始向上移動
                if self.body.linearVelocity[1] > 0:
                    #向上移動
                    if self.body.position[1] > self.end_position[1] - self.init_position[1]:
                        self.body.linearVelocity[1] = self.velocity[1] * -1
                elif self.body.linearVelocity[1] < 0:
                    if self.body.position[1] < 0:
                        self.body.linearVelocity[1] = self.velocity[1]
                else:
                    pass
            pass
        else:
            pass
    def get_polygon_vertice(self):
        # Box2D
        self.vertices = [(self.body.transform * v) for v in self.box.shape.vertices]
        self.pixel_vertices = [(self.body.transform * v) * PPM * self.maze_size for v in self.box.shape.vertices]
        self.pixel_vertices = [(v[0], HEIGHT - v[1]) for v in self.pixel_vertices]

    def get_wall_infomation(self):
        self.wall_info = []
        self.wall_info.append([self.vertices[0],self.vertices[1]])
        self.wall_info.append([self.vertices[2],self.vertices[1]])
        self.wall_info.append([self.vertices[3],self.vertices[0]])
        self.wall_info.append([self.vertices[2],self.vertices[3]])

class Check_point:
    def __init__(self):
        pass

    def collide_with_car(self):
        pass
