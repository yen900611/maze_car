import random
from .math_function import *
import pygame
import Box2D
from .env import *

class Sensor():
    def __init__(self, world, body):
        self.car = body
        self.right_value = 0
        self.left_value = 0
        self.front_value = 0
        self.sensor_right = world.CreateDynamicBody(position=(body.position[0] + 1, body.position[1]))
        ball = self.sensor_right.CreateCircleFixture(radius=0.1)
        self.sensor_left = world.CreateDynamicBody(position=(body.position[0] - 1, body.position[1]))
        ball = self.sensor_left.CreateCircleFixture(radius=0.1)
        world.CreateDistanceJoint(bodyA=self.sensor_left, bodyB=body, anchorA=self.sensor_left.position,
                                  anchorB=body.position, collideConnected=True)
        world.CreateDistanceJoint(bodyA=self.sensor_right, bodyB=body, anchorA=self.sensor_right.position,
                                  anchorB=body.position, collideConnected=True)
        self.last_detect_sensor = -3
        pass

    def update(self, frame, walls):
        if frame - self.last_detect_sensor > FPS / 15:
            self.front_sensor_detect(walls)
            self.sensor_detect(walls)
            self.last_detect_sensor = frame
            pass
        return {"right_value": self.right_value,
                "left_value": self.left_value,
                "front_value": self.front_value}

    def front_sensor_detect(self, walls):
        car_center = self.car.position
        distance = []
        results = []
        dots = []
        vector = None
        if self.sensor_left.position[0] == self.sensor_right.position[0]:
            vector = [1, 0]
        elif self.sensor_left.position[1] == self.sensor_right.position[1]:
            vector = [0, 1]
        else:
            vector = (
                self.sensor_left.position[1] - self.sensor_right.position[1],
                self.sensor_right.position[0] - self.sensor_left.position[0])

        for wall in walls:
            distance.append(cross_point_dot(car_center,
                                            vector,
                                            wall[0], wall[1]))
        for i in distance:
            if i:
                if i[0] - car_center[0] > 0 and vector[0] > 0:
                    results.append(math.sqrt(
                        (i[0] - car_center[0]) ** 2 + (i[1] - car_center[1]) ** 2) - 1.5)
                    dots.append(i)
                elif i[0] - car_center[0] < 0 and vector[0] < 0:
                    results.append(math.sqrt(
                        (i[0] - car_center[0]) ** 2 + (i[1] - car_center[1]) ** 2) - 1.5)
                    dots.append(i)
                else:
                    pass
            else:
                pass

        try:
            self.front_value = round(min(results) * 5 * random.uniform(0.95, 1.05), 1)
            if self.front_value < 0:
                self.front_value = 0
        except TypeError:
            self.front_value = -1
        except ValueError:
            self.front_value = -1

    def sensor_detect(self, walls):
        r_distance = []
        l_distance = []
        dots = []
        r_dots = []
        l_dots = []

        for wall in walls:
            dots.append(cross_point_dot(self.sensor_right.position,
                                        self.sensor_left.position - self.sensor_right.position,
                                        wall[0], wall[1])
                        )
        for i in dots:
            if i:
                if self.sensor_left.position[0] > self.sensor_right.position[0] >= i[0]:
                    # 車子面朝Y軸負向，此點位於車體右方
                    r_dots.append(i)
                    r_distance.append(
                        math.sqrt((i[0] - self.sensor_right.position[0]) ** 2 + (
                                i[1] - self.sensor_right.position[1]) ** 2))
                elif i[0] >= self.sensor_right.position[0] > self.sensor_left.position[0]:
                    # 車子面朝Y軸正向，此點位於車體右方
                    r_dots.append(i)
                    r_distance.append(
                        math.sqrt((i[0] - self.sensor_right.position[0]) ** 2 + (
                                i[1] - self.sensor_right.position[1]) ** 2))
                elif self.sensor_right.position[0] > self.sensor_left.position[0] >= i[0]:
                    # 車子面朝Y軸正向，此點位於車體左方
                    l_dots.append(i)
                    l_distance.append(
                        math.sqrt((i[0] - self.sensor_left.position[0]) ** 2 + (
                                i[1] - self.sensor_left.position[1]) ** 2))
                elif i[0] >= self.sensor_left.position[0] > self.sensor_right.position[0]:
                    # 車子面朝Y軸負向，此點位於車體左方
                    l_dots.append(i)
                    l_distance.append(
                        math.sqrt((i[0] - self.sensor_left.position[0]) ** 2 + (
                                i[1] - self.sensor_left.position[1]) ** 2))
                else:
                    pass

        try:
            self.right_value = round(min(r_distance) * 5 * random.uniform(0.95, 1.05), 1)
            self.left_value = round(min(l_distance) * 5 * random.uniform(0.95, 1.05), 1)

        except TypeError:
            self.right_value = -1
            self.left_value = -1
        except ValueError:
            self.right_value = -1
            self.left_value = -1
