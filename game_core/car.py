from .math_function import cross_point_dot
import math

from .sensor import Sensor
import pygame
from .env import *


class Car(pygame.sprite.Sprite):
    def __init__(self, world, position: tuple, car_no: int, size):
        pygame.sprite.Sprite.__init__(self)
        self.car_no = car_no  # From 0 to 5
        self.maze_size = size  # 4/size of maze
        self.size = (int(50 * self.maze_size), int(40 * self.maze_size))  # car size
        self.end_time = 0
        self.score = 0 # 積分
        self.origin_image = pygame.transform.scale(
            pygame.image.load(path.join(IMAGE_DIR, "car_0" + str(self.car_no + 1) + ".png")),
            self.size)
        self.image = self.origin_image  # after rotate
        self.rect = self.image.get_rect()
        self.status = True
        self.sensor_R = 0
        self.sensor_L = 0
        self.sensor_F = 0
        self.L_PWM = 0
        self.R_PWM = 0
        self.rect.center = (0, 0)  # pygame
        self.body = world.CreateDynamicBody(position=position)
        self.box1 = self.body.CreatePolygonFixture(box=(0.9, 0.9), density=1, friction=0.1, restitution=0.3)
        self.vertices = []  # pygame
        self.sensor = Sensor(world, self.body)

        '''模擬摩擦力'''
        # r = math.sqrt(2.0 * self.body.inertia / self.body.mass)
        # gravity = 10
        # ground = world.CreateBody(position=(0, 20))
        # world.CreateFrictionJoint(
        #     bodyA=ground,
        #     bodyB=self.body,
        #     localAnchorA=(0, 0),
        #     localAnchorB=(0, 0),
        #     collideConnected=True,
        #     maxForce=self.body.mass * r * gravity * 4,
        #     maxTorque=self.body.mass * r * gravity
        # )
        pass

    def update(self, commands):
        self.get_polygon_vertice()
        if self.status and commands != None:
            if commands[0]['right_PWM'] > 255:
                self.R_PWM = 255
            elif commands[0]['right_PWM'] < -255:
                self.R_PWM = -255
            else:
                self.R_PWM = commands[0]['right_PWM']
            if commands[0]['left_PWM'] > 255:
                self.L_PWM = 255
            elif commands[0]['left_PWM'] < -255:
                self.L_PWM = -255
            else:
                self.L_PWM = commands[0]['left_PWM']
            self.right_move(self.R_PWM)
            self.left_move(self.L_PWM)

    def detect_distance(self, frame, walls):
        sensor_value = self.sensor.update(frame, walls)
        self.sensor_R = sensor_value["right_value"]
        self.sensor_L = sensor_value["left_value"]
        self.sensor_F = sensor_value["front_value"]
        pass

    def left_move(self, pwm: int):
        if pwm <0:
            self.sensor.sensor_left.linearVelocity = self.body.GetWorldVector(localVector=(0, -(abs(pwm) ** 0.5)))
        else:
            self.sensor.sensor_left.linearVelocity =self.body.GetWorldVector(localVector = (0,pwm**0.5))

    def right_move(self, pwm: int):
        if pwm <0:
            self.sensor.sensor_right.linearVelocity = self.body.GetWorldVector(localVector=(0, -(abs(pwm) ** 0.5)))
        else:
            self.sensor.sensor_right.linearVelocity =self.body.GetWorldVector(localVector = (0,pwm**0.5))

    def keep_in_screen(self):
        pass

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "size": self.size,  # pygame
                         "center": self.rect.center,  # pygame
                         "vertices": self.vertices,  # pygame
                         "angle": self.body.angle,  # Box2D
                         "r_sensor_value": self.sensor_R,
                         "l_sensor_value": self.sensor_L,
                         "f_sensor_value": self.sensor_F,
                         "L_PWM": self.L_PWM,
                         "R_PWM":self.R_PWM
                         }
        return self.car_info

    def get_polygon_vertice(self):
        self.vertices = [(self.body.transform * v) * PPM * self.maze_size for v in self.box1.shape.vertices]
        self.vertices = [(v[0], HEIGHT - v[1]) for v in self.vertices]
        self.image = pygame.transform.rotate(self.origin_image, (self.body.angle * 180 / math.pi) % 360)
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * PPM * self.maze_size, HEIGHT - self.body.position[
            1] * PPM * self.maze_size
