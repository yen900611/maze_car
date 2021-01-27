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
        if self.is_move:
            print(self.end_position, self.init_position)

    def update(self) -> None:
        self.get_polygon_vertice()
        self.get_wall_infomation()
        # self.count_position(self.vertices)
        if self.is_move:
            # print(self.pixel_vertices)
            # print(self.wall_info)
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
        if self.body.linearVelocity[0] < 0:
            if self.body.position[0] < self.end_position[0] - self.init_position[0]:
                self.body.linearVelocity[0] = self.velocity[0] * -1
        elif self.body.linearVelocity[0] > 0:
            if self.body.position[0] > 0:
                self.body.linearVelocity[0] = self.velocity[0]
        else:
            pass
    def get_polygon_vertice(self):
        # Box2D
        self.vertices = [(self.body.transform * v) for v in self.box.shape.vertices]
        self.pixel_vertices = [(self.body.transform * v) * PPM * self.maze_size for v in self.box.shape.vertices]
        self.pixel_vertices = [(v[0], HEIGHT - v[1]) for v in self.pixel_vertices]
        # self.image = pygame.transform.rotate(self.origin_image, (self.body.angle * 180 / math.pi) % 360)
        # self.rect = self.image.get_rect()
        # self.rect.center = self.body.position[0] * PPM * self.maze_size, HEIGHT - self.body.position[
        #     1] * PPM * self.maze_size

    def get_wall_infomation(self):
        self.wall_info = []
        self.wall_info.append([self.vertices[0],self.vertices[1]])
        self.wall_info.append([self.vertices[2],self.vertices[1]])
        self.wall_info.append([self.vertices[3],self.vertices[0]])
        self.wall_info.append([self.vertices[2],self.vertices[3]])
        pass


