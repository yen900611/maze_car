import Box2D

from .gameMode import GameMode
from .env import *
import pygame
import random

class PlayingMode(GameMode):
    def __init__(self, user_num: int, sound_controller):
        super(PlayingMode, self).__init__()
        pygame.font.init()
        self.status = None
        self.worlds = []
        self._init_world(user_num)
        self._init_maze(0)

        '''sound'''
        self.sound_controller = sound_controller

        '''image'''
        self.cars_info = []
        self.sensor_value = []

    def update_sprite(self, command):
        '''update the model of game,call this fuction per frame'''
        self.frame += 1
        self.handle_event()
        for world in self.worlds:
            world.Step(TIME_STEP, 10, 10)

    def detect_collision(self):
        super(PlayingMode,self).detect_collision()
        pass

    def _print_result(self):
        pass

    def _init_world(self, user_no: int):
        for i in range(user_no):
            world = Box2D.b2.world(gravity=(0, 0), doSleep=True, CollideConnected=False)
            self.worlds.append(world)
        pass

    def _init_car(self, world):
        for world in self.worlds:
            pass

    def _init_maze(self, maze_no):
        for world in self.worlds:
            for wall in Maze[maze_no]:
                wall_bottom = world.CreateKinematicBody(position=(0, 0), linearVelocity=(0, 0))
                box = wall_bottom.CreatePolygonFixture(vertices=wall)
        pass

    def _is_game_end(self):
        pass

    def _is_car_arrive_end(self, car):
        pass

    def draw_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(PlayingMode, self).draw_bg()
        pass

        '''畫出每台車子的資訊'''
        self._draw_user_imformation()

    def drawWorld(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(PlayingMode,self).drawWorld()

        def my_draw_circle(circle, body, fixture):
            position = body.transform * circle.pos * PPM
            position = (position[0], HEIGHT - position[1])
            pygame.draw.circle(self.screen, WHITE, [int(
                x) for x in position], int(circle.radius * PPM))

        def my_draw_polygon(polygon, body, fixture):
            vertices = [(body.transform * v) * PPM for v in polygon.vertices]
            vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(self.screen, GREY, vertices)

        Box2D.b2.polygonShape.draw = my_draw_polygon
        Box2D.b2.circleShape.draw = my_draw_circle

        for world in self.worlds:
            for body in world.bodies:
                for fixture in body.fixtures:
                    fixture.shape.draw(body, fixture)
        pass

    def _draw_user_imformation(self):
        pass

    def rank(self):
        pass
