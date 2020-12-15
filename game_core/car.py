import math

from .sensor import Sensor
import pygame
import Box2D
import time
from .env import *
import random

class Car():
    def __init__(self, world, position:tuple, car_no:int):
        self.car_no = car_no
        self.velocity = 0
        self.body = world.CreateDynamicBody(position=position)
        box1 = self.body.CreatePolygonFixture(box=(1, 1), density=2, friction=0.1, restitution=0.3)
        self.sensor_right = Sensor(world, (position[0]+1, position[1]))
        self.sensor_left = Sensor(world, (position[0]-1, position[1]))
        world.CreateDistanceJoint(bodyA=self.sensor_left.body, bodyB=self.body, collideConnected=True)
        world.CreateDistanceJoint(bodyA=self.sensor_right.body, bodyB=self.body, collideConnected=True)
        r = math.sqrt(0.2 * self.body.inertia / self.body.mass)
        '''模擬摩擦力'''
        gravity = 0.5
        ground = world.CreateBody(position=(0, 20))
        world.CreateFrictionJoint(
            bodyA=ground,
            bodyB=self.body,
            localAnchorA=(0, 0),
            localAnchorB=(0, 0),
            collideConnected=True,
            maxTorque=self.body.mass * r * gravity
        )
        pass

    def update(self, commands):
        if SPEED_cmd in commands:
            pass
        elif BRAKE_cmd in commands:
            pass
        else:
            pass
        for command in commands:
            if LEFT_cmd == command:
                self.turn_Left()
            if RIGHT_cmd == command:
                self.turn_Right()
        pass

    def speedUp(self, next_velocity):
        print("speed")
        f = self.body.GetWorldVector(localVector=(0.0, 200.0))
        p = self.body.GetWorldPoint(localPoint=(0.0, -2.0))
        self.body.ApplyForce(f, p, True)

    def brakeDown(self, next_velocity):
        print("down")
        f = self.body.GetWorldVector(localVector=(0.0, -200.0))
        p = self.body.GetWorldPoint(localPoint=(0.0, -2.0))
        self.body.ApplyForce(f, p, True)

    def turn_Right(self):
        self.body.ApplyTorque(-40.0, True)

    def turn_Left(self):
        self.body.ApplyTorque(40.0, True)

    def keep_in_screen(self):
        pass

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "pos": (self.rect.left, self.rect.top),
                         }
        return self.car_info
