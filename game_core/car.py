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
        self.image = pygame.image.load(path.join(IMAGE_DIR, "car_0" + str(self.car_no+1) +".png"))
        self.sensor_R = 0
        self.sensor_L = 0
        self.sensor_F = 0
        self.velocity = 0
        self.body = world.CreateDynamicBody(position=position)
        box1 = self.body.CreatePolygonFixture(box=(0.9, 0.9), density=2, friction=0.1, restitution=0.3)
        self.sensor_right = Sensor(world, (position[0]+0.45, position[1]))
        self.sensor_left = Sensor(world, (position[0]-0.45, position[1]))
        world.CreateDistanceJoint(bodyA=self.sensor_left.body, bodyB=self.body, collideConnected=True)
        world.CreateDistanceJoint(bodyA=self.sensor_right.body, bodyB=self.body, collideConnected=True)

        '''模擬摩擦力'''
        r = math.sqrt(0.2 * self.body.inertia / self.body.mass)
        gravity = 10
        ground = world.CreateBody(position=(0, 20))
        world.CreateFrictionJoint(
            bodyA=ground,
            bodyB=self.body,
            localAnchorA=(0, 0),
            localAnchorB=(0, 0),
            collideConnected=True,
            maxForce = self.body.mass * r * gravity,
            maxTorque=self.body.mass * r * gravity
        )
        pass

    def update(self, commands):
        self.velocity =math.sqrt(self.body.linearVelocity[0] ** 2 + self.body.linearVelocity[1] ** 2)
        if commands[0]['left_PWM'] == 0:
            self.body.localCenter = (-0.3, 0)
            self.right_move(commands[0]['right_PWM'])
        elif commands[0]['right_PWM'] == 0:
            self.body.localCenter = (0.3, 0)
            self.left_move(commands[0]['left_PWM'])
        else:
            self.right_move(commands[0]['right_PWM'])
            self.left_move(commands[0]['left_PWM'])
        self.sensor_F = self.front_sensor_detect(wall_info)
        self.sensor_L = self.left_sensor_detect(wall_info)
        self.sensor_R = self.right_sensor_detect(wall_info)
        pass

    def left_move(self, velocity:int):
        if self.velocity > 0.01:
            f = self.body.GetWorldVector(localVector=(0.0, velocity/self.velocity))
        else:
            f = self.body.GetWorldVector(localVector=(0.0, velocity))
        p = self.body.GetWorldPoint(localPoint=(-1.0, 0.0))
        self.body.ApplyForce(f, p, False)

    def right_move(self, velocity:int):
        if self.velocity > 0.01:
            f = self.body.GetWorldVector(localVector=(0.0, velocity/self.velocity))
        else:
            f = self.body.GetWorldVector(localVector=(0.0, velocity))
        p = self.body.GetWorldPoint(localPoint=(1.0, 0.0))
        self.body.ApplyForce(f, p, False)


    def keep_in_screen(self):
        pass

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "pos": self.body.position,
                         "angle":self.body.angle,
                         }
        return self.car_info

    def front_sensor_detect(self, walls):
        distance = []
        results = []
        dots = []
        vector = None
        if self.sensor_left.body.position[0] == self.sensor_right.body.position[0]:
            vector = (1, 0)
        elif self.sensor_left.body.position[1] == self.sensor_right.body.position[1]:
            vector = (0, 1)
        else:
            vector = (
            self.sensor_left.body.position[1] - self.sensor_right.body.position[1], self.sensor_right.body.position[0] - self.sensor_left.body.position[0])

        for wall in walls:
            distance.append(self.cross_point_dot(self.body.position,
                                            vector,
                                            wall[0], wall[1]))
        for i in distance:
            if i:
                if i[0] - self.body.position[0] > 0 and vector[0] > 0:
                    results.append(math.sqrt(
                        (i[0] - self.body.position[0]) ** 2 + (i[1] - self.body.position[1]) ** 2) - 1.5)
                    dots.append(i)
                elif i[0] - self.body.position[0] < 0 and vector[0] < 0:
                    results.append(math.sqrt(
                        (i[0] - self.body.position[0]) ** 2 + (i[1] - self.body.position[1]) ** 2) - 1.5)
                    dots.append(i)
                else:
                    pass
            else:
                pass

        try:
            result = round(min(results)*5,1)
            return result
        except TypeError:
            return round(random.randrange(30.0), 1)
        except ValueError:
            return round(random.randrange(30.0), 1)

    def right_sensor_detect(self, walls):
        distance = []
        results = []
        dots = []
        for wall in walls:
            distance.append(self.cross_point_dot(self.sensor_right.body.position,
                                            self.sensor_left.body.position - self.sensor_right.body.position,
                                            wall[0], wall[1])
                            )
        for i in distance:
            if i:
                if self.sensor_left.body.position[0] > self.sensor_right.body.position[0] >= i[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_right.body.position[0]) ** 2 + (i[1] - self.sensor_right.body.position[1]) ** 2))
                elif i[0] >= self.sensor_right.body.position[0] > self.sensor_left.body.position[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_right.body.position[0]) ** 2 + (i[1] - self.sensor_right.body.position[1]) ** 2))
                else:
                    pass

        try:
            result = round(min(results)*5,1)
            return result
        except TypeError:
            return None
        except ValueError:
            return None

    def left_sensor_detect(self, walls):
        distance = []
        results = []
        dots = []
        for wall in walls:
            distance.append(self.cross_point_dot(self.sensor_left.body.position,
                                            self.sensor_right.body.position - self.sensor_left.body.position,
                                            wall[0], wall[1])
                            )
        for i in distance:
            if i:
                if self.sensor_right.body.position[0] > self.sensor_left.body.position[0] >= i[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_left.body.position[0]) ** 2 + (i[1] - self.sensor_left.body.position[1]) ** 2))
                elif i[0] >= self.sensor_left.body.position[0] > self.sensor_right.body.position[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_left.body.position[0]) ** 2 + (i[1] - self.sensor_left.body.position[1]) ** 2))
                else:
                    pass
        try:

            result = round(min(results)*5, 1)
            return result
        except TypeError:
            return None
        except ValueError:
            return None
    def cross_point(self, dot1, vec1, dot2, vec2):
        '''
        define line A and line B, write a function which can return the point two lines cross.
        dot_1 = (x1, y1)
        dot_2 = (x2, y2)
        vec_1 = (vx1, vy1)
        vec_2 = (vx2, vy2)
        line1 = [(x1, y1), (x1 + vx1, y1 + vy1)], line2 = [(x2, y2), (x2 + vx2, y2 + vy2)]
        '''
        x1 = dot1[0]
        y1 = dot1[1]
        x2 = dot2[0]
        y2 = dot2[1]
        vx1 = vec1[0]
        vy1 = vec1[1]
        vx2 = vec2[0]
        vy2 = vec2[1]
        if vx1 == 0:  # 如果斜率為0
            k1 = None
            b1 = 0
        else:
            k1 = vy1 * 1.0 / vx1
            b1 = (y1 + vy1) * 1.0 - (x1 + vx1) * k1 * 1.0
        if vx2 == 0:
            k2 = None
            b2 = 0
        else:
            k2 = vy2 * 1.0 / vx2
            b2 = (y2 + vy2) * 1.0 - (x2 + vx2) * k2 * 1.0

        if k1 == k2:
            return None
        elif k1 == None:  # 如果Line1斜率不存在，則取Line1上的點帶入Line2的公式
            x = x1 + vx1
            k1 = k2
            b1 = b2
        elif k2 == None:
            x = x2 + vx2
        else:
            x = (b2 - b1) * 1.0 / (k1 - k2)
        y = k1 * x * 1.0 + b1 * 1.0
        return (x, y)

    def cross_point_dot(self, dot1, vec1, dot2, dot3):
        '''
        this function is same as above. But in this case, one of lines has starting point and ending point.
        If the point two line cross out of the line, function should return None.
        '''
        x2 = dot2[0]
        y2 = dot2[1]
        x3 = dot3[0]
        y3 = dot3[1]
        p = self.cross_point(dot1, vec1, dot2, (x3 - x2, y3 - y2))
        if p:
            if x2 <= p[0] <= x3 or x3 <= p[0] <= x2:
                if y2 <= p[1] <= y3 or y3 <= p[1] <= y2:
                    return p
                else:
                    return None
        else:
            return None