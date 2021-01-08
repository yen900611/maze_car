from .math_function import cross_point_dot
import math

from .sensor import Sensor
import pygame
from .env import *
import random


class Car():
    def __init__(self, world, position: tuple, car_no: int, size):
        self.car_no = car_no
        self.maze_size = size
        self.size = (int(50 * self.maze_size), int(40 * self.maze_size))
        self.end_time = 0
        self.image = pygame.transform.scale(
            pygame.image.load(path.join(IMAGE_DIR, "car_0" + str(self.car_no + 1) + ".png")),
            self.size)
        self.status = True
        self.sensor_R = 0
        self.sensor_L = 0
        self.sensor_F = 0
        self.velocity = 0
        self.center_position = (0, 0)
        self.body = world.CreateDynamicBody(position=position)
        self.box1 = self.body.CreatePolygonFixture(box=(0.9, 0.9), density=2, friction=0.1, restitution=0.3)
        self.vertices = []
        self.sensor = Sensor(world, self.body)

        '''模擬摩擦力'''
        r = math.sqrt(0.5 * self.body.inertia / self.body.mass)
        gravity = 10
        ground = world.CreateBody(position=(0, 20))
        world.CreateFrictionJoint(
            bodyA=ground,
            bodyB=self.body,
            localAnchorA=(0, 0),
            localAnchorB=(0, 0),
            collideConnected=True,
            maxForce=self.body.mass * r * gravity * 1.5,
            maxTorque=self.body.mass * r * 5
        )
        pass

    def update(self, commands):
        self.get_polygon_vertice()
        self.velocity = math.sqrt(self.body.linearVelocity[0] ** 2 + self.body.linearVelocity[1] ** 2)
        if self.status:
            current_forward_normal = self.body.GetWorldVector((0, 1))
            self.right_move(commands[0]['right_PWM'])
            self.left_move(commands[0]['left_PWM'])

            # if commands[0]['left_PWM'] == 0:
            #     self.body.localCenter = (-0.3, 0)
            #     self.right_move(commands[0]['right_PWM'])
            # elif commands[0]['right_PWM'] == 0:
            #     self.body.localCenter = (0.3, 0)
            #     self.left_move(commands[0]['left_PWM'])
            # else:
            #     self.right_move(commands[0]['right_PWM'])
            #     self.left_move(commands[0]['left_PWM'])

    def detect_distance(self, frame, maze_id):
        sensor_value = self.sensor.update(frame,maze_id)
        self.sensor_R = sensor_value["right_value"]
        self.sensor_L = sensor_value["left_value"]
        self.sensor_F = sensor_value["front_value"]
        pass

    def left_move(self, pwm: int):
        if self.velocity > 0.01:
            f = self.body.GetWorldVector(localVector=(0.0, pwm / self.velocity))
        else:
            f = self.body.GetWorldVector(localVector=(0.0, pwm))

        p = self.body.GetWorldPoint(localPoint=(-1.0, 0.0))
        self.body.ApplyForce(f, p, True)

    def right_move(self, pwm: int):


        if self.velocity > 0.01:
            f = self.body.GetWorldVector(localVector=(0.0, pwm / self.velocity))
        else:
            f = self.body.GetWorldVector(localVector=(0.0, pwm))

        p = self.body.GetWorldPoint(localPoint=(1.0, 0.0))
        self.body.ApplyForce(f, p, True)

    def keep_in_screen(self):
        pass

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "size": self.size,
                         "center": self.center_position,
                         "vertices": self.vertices,
                         "angle": self.body.angle,
                         "r_sensor_value": self.sensor_R,
                         "l_sensor_value": self.sensor_L,
                         "f_sensor_value": self.sensor_F,
                         }
        return self.car_info

    def get_polygon_vertice(self):
        self.vertices = [(self.body.transform * v) * PPM * self.maze_size for v in self.box1.shape.vertices]
        self.vertices = [(v[0], HEIGHT - v[1]) for v in self.vertices]
        self.center_position = self.body.position[0] * PPM * self.maze_size, HEIGHT - self.body.position[
            1] * PPM * self.maze_size
        pass
