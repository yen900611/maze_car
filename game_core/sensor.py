import random
from .math_function import *
import pygame
import Box2D
from .env import *

class Sensor():
    def __init__(self, world, body):
        self.car = body
        self.right_value = {}
        self.left_value = {}
        self.front_value = {}
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
        self.front_sensor_detect(walls)
        self.sensor_detect(walls)
        self.last_detect_sensor = frame
        if frame - self.last_detect_sensor > 2:
            self.sensor_right.position = self.car.GetWorldVector(localVector=(1, 0)) + self.car.position
            self.sensor_left.position = self.car.GetWorldVector(localVector=(-1, 0)) + self.car.position
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
        for dot in distance:
            if dot:
                if dot[0] - car_center[0] > 0 and vector[0] > 0:
                    results.append(math.sqrt(
                        (dot[0] - car_center[0]) ** 2 + (dot[1] - car_center[1]) ** 2) - 1.5)
                    dots.append(dot)
                elif dot[0] - car_center[0] < 0 and vector[0] < 0:
                    results.append(math.sqrt(
                        (dot[0] - car_center[0]) ** 2 + (dot[1] - car_center[1]) ** 2) - 1.5)
                    dots.append(dot)
                else:
                    pass
            else:
                pass

        try:
            self.front_value = {"coordinate":dots[results.index(min(results))],
                                "distance":round(min(results) * 5 * random.uniform(0.95, 1.05), 1),
                                "all_dots":dots}
            # self.front_value = round(min(results) * 5 * random.uniform(0.95, 1.05), 1)
            if self.front_value["distance"] < 0:
                self.front_value["distance"] = 0
        except TypeError:
            self.front_value["distance"] = -1
        except ValueError:
            self.front_value["distance"] = -1

    def sensor_detect(self, walls):
        r_distance = []
        l_distance = []
        dots = []
        r_dots = []
        l_dots = []
        position = self.sensor_left.position - self.sensor_right.position
        for wall in walls:
            dots.append(cross_point_dot(self.sensor_right.position,
                                        position,
                                        wall[0], wall[1])
                        )
        for dot in dots:
            if dot:
                if self.sensor_left.position[0] > self.sensor_right.position[0] >= dot[0]:
                    # 車子面朝Y軸負向，此點位於車體右方
                    r_dots.append(dot)
                    r_distance.append(
                        math.sqrt((dot[0] - self.sensor_right.position[0]) ** 2 + (
                                dot[1] - self.sensor_right.position[1]) ** 2))
                elif dot[0] >= self.sensor_right.position[0] > self.sensor_left.position[0]:
                    # 車子面朝Y軸正向，此點位於車體右方
                    r_dots.append(dot)
                    r_distance.append(
                        math.sqrt((dot[0] - self.sensor_right.position[0]) ** 2 + (
                                dot[1] - self.sensor_right.position[1]) ** 2))
                elif self.sensor_right.position[0] > self.sensor_left.position[0] >= dot[0]:
                    # 車子面朝Y軸正向，此點位於車體左方
                    l_dots.append(dot)
                    l_distance.append(
                        math.sqrt((dot[0] - self.sensor_left.position[0]) ** 2 + (
                                dot[1] - self.sensor_left.position[1]) ** 2))
                elif dot[0] >= self.sensor_left.position[0] > self.sensor_right.position[0]:
                    # 車子面朝Y軸負向，此點位於車體左方
                    l_dots.append(dot)
                    l_distance.append(
                        math.sqrt((dot[0] - self.sensor_left.position[0]) ** 2 + (
                                dot[1] - self.sensor_left.position[1]) ** 2))
                else:
                    pass

        try:
            self.right_value = {"coordinate":r_dots[r_distance.index(min(r_distance))],
                                "distance":round(min(r_distance) * 5 * random.uniform(0.95, 1.05), 1),
                                "all_dots":r_dots}
            self.left_value = {"coordinate":l_dots[l_distance.index(min(l_distance))],
                               "distance":round(min(l_distance) * 5 * random.uniform(0.95, 1.05), 1),
                               "all_dots":l_dots}

            # self.right_value = round(min(r_distance) * 5 * random.uniform(0.95, 1.05), 1)
            # self.left_value = round(min(l_distance) * 5 * random.uniform(0.95, 1.05), 1)

        except TypeError:
            self.right_value["distance"] = -1
            self.left_value["distance"] = -1
        except ValueError:
            self.right_value["distance"] = -1
            self.left_value["distance"] = -1
