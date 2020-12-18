import math

import Box2D
from .car import Car
from .gameMode import GameMode
from .env import *
import pygame
import random

class PlayingMode(GameMode):
    def __init__(self, user_num: int, sound_controller):
        super(PlayingMode, self).__init__()
        pygame.font.init()
        self.status = None

        '''set group'''
        self.cars = []

        self.worlds = []
        self._init_world(user_num)
        self._init_car()
        self._init_maze(0)


        '''sound'''
        self.sound_controller = sound_controller

        '''image'''
        self.info = pygame.image.load(path.join(IMAGE_DIR, info_image))
        self.sensor_value = []

    def update_sprite(self, command):
        '''update the model of game,call this fuction per frame'''
        # print(command)
        self.frame += 1
        self.handle_event()
        for car in self.cars:
            car.update(command["ml_" + str(car.car_no+1) + "P"])
        for world in self.worlds:
            world.Step(TIME_STEP, 10, 10)
            world.ClearForces()

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

    def _init_car(self):
        for world in self.worlds:
            self.car = Car(world, (22,3), 0)
            self.cars.append(self.car)
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
        self.screen.fill(BLACK)
        # pygame.draw.rect(self.screen, BROWN, pygame.Rect(20,20,480,480))
        self.screen.blit(self.info,pygame.Rect(507, 20, 306, 480))
        # pygame.draw.rect(self.screen, WHITE, pygame.Rect((520, 20), (280, 480)), border_radius=20)
        # pygame.draw.rect(self.screen, BLUE, pygame.Rect((525, 25), (270, 470)), border_radius=20)
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
            pygame.draw.polygon(self.screen, WHITE, vertices)

        Box2D.b2.polygonShape.draw = my_draw_polygon
        Box2D.b2.circleShape.draw = my_draw_circle

        for world in self.worlds:
            for body in world.bodies:
                for fixture in body.fixtures:
                    fixture.shape.draw(body, fixture)
        for car in self.cars:
            image = pygame.transform.rotate(car.image,(car.body.angle*180/math.pi)%360)
            rect = image.get_rect()
            rect.center = car.body.position[0] * PPM, HEIGHT - car.body.position[1] * PPM
            self.screen.blit(image, rect)
            pass
        pass

    def _draw_user_imformation(self):
        for i in range(3):
            for car in self.cars:
                if car.car_no == i:
                    # pygame.draw.line(self.screen, RED, (car.sensor_right.body.position[0]*PPM, HEIGHT - car.sensor_right.body.position[1]*PPM),
                    #                  (car.sensor_R[0]*PPM, HEIGHT - car.sensor_R[1]*PPM),2)
                    self.draw_information(self.screen, WHITE, "R:" + str(car.sensor_R), 600, 178 + 20 + 94*i)
                    self.draw_information(self.screen, WHITE, "L:" + str(car.sensor_L), 600, 178 + 40 + 94*i)
                    self.draw_information(self.screen, WHITE, "F:" + str(car.sensor_F), 600, 178 + 60 + 94*i)

        for i in range(3):
            self.draw_information(self.screen, WHITE, "R:", 730, 178 + 20 + 94*i)
            self.draw_information(self.screen, WHITE, "L:", 730, 178 + 40 + 94*i)
            self.draw_information(self.screen, WHITE, "F:", 730, 178 + 60 + 94*i)
        pass

    def rank(self):
        pass
