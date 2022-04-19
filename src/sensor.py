import random
from .math_function import *
import pygame
import Box2D
from .env import *

class Sensor():
    def __init__(self, world, body, sensor_num, angle):
        self.car = body
        self.right_value = {}
        self.right_top_value = {}
        self.left_value = {}
        self.left__top_value = {}
        self.front_value = {}
        self.sensor_num = sensor_num
        angle_t = int(angle/0.5)%4
        self.sensor_right = world.CreateDynamicBody(position=(body.position[0] + sensor_trans[angle_t][0], body.position[1]+ sensor_trans[angle_t][1]))
        ball = self.sensor_right.CreateCircleFixture(radius=0.1)
        self.sensor_left = world.CreateDynamicBody(position=(body.position[0] - sensor_trans[angle_t][0], body.position[1] - sensor_trans[angle_t][1]))
        ball = self.sensor_left.CreateCircleFixture(radius=0.1)

        world.CreateDistanceJoint(bodyA=self.sensor_left, bodyB=body, anchorA=self.sensor_left.position,
                                  anchorB=body.position, collideConnected=True)
        world.CreateDistanceJoint(bodyA=self.sensor_right, bodyB=body, anchorA=self.sensor_right.position,
                                  anchorB=body.position, collideConnected=True)
        self.last_detect_sensor = -3
        pass

    def update(self, frame, walls):
        self.front_value = self.sensor_detect(walls, (0, 1))
        self.right_value = self.sensor_detect(walls, (1, 0))
        self.left_value = self.sensor_detect(walls, (-1, 0))
        if self.sensor_num == 5:
            self.right_top_value = self.sensor_detect(walls, (1, 1))
            self.left_top_value = self.sensor_detect(walls, (-1, 1))
        else:
            self.right_top_value = {"coordinate":self.car.position,
                            "distance": -1}
            self.left_top_value = {"coordinate":self.car.position,
                            "distance": -1}

        self.last_detect_sensor = frame
        if frame - self.last_detect_sensor > 2:
            self.sensor_right.position = self.car.GetWorldVector(localVector=(1, 0)) + self.car.position
            self.sensor_left.position = self.car.GetWorldVector(localVector=(-1, 0)) + self.car.position
            pass
        return {"right_value": self.right_value,
                "left_value": self.left_value,
                "front_value": self.front_value,
                "right_top_value": self.right_top_value,
                "left_top_value": self.left_top_value}

    def sensor_detect(self, walls, vector):
        car_center = self.car.position
        distance = []
        results = []
        dots = []
        vector = self.car.GetWorldVector(localVector = vector)
        sensor_value = {}

        for wall in walls:
            distance.append(cross_point_dot(car_center,
                                            vector,
                                            wall[0], wall[1]))
        for dot in distance:
            if dot:
                if dot[0] - car_center[0] > 0 and vector[0] > 0:
                    results.append(math.sqrt(
                        (dot[0] - car_center[0]) ** 2 + (dot[1] - car_center[1]) ** 2) - 1)
                    dots.append(dot)
                elif dot[0] - car_center[0] < 0 and vector[0] < 0:
                    results.append(math.sqrt(
                        (dot[0] - car_center[0]) ** 2 + (dot[1] - car_center[1]) ** 2) - 1)
                    dots.append(dot)
                else:
                    pass
            else:
                pass

        try:
            coordinate = dots[results.index(min(results))]
            sensor_value = {"coordinate":(round(coordinate[0], 3), round(coordinate[1], 3)),
                            "distance":round(min(results) * 5 * random.uniform(0.95, 1.05), 1)
                            }
            # self.front_value = round(min(results) * 5 * random.uniform(0.95, 1.05), 1)
            if sensor_value["distance"] < 0:
                sensor_value["distance"] = 0
            return sensor_value
        except TypeError:
            sensor_value["distance"] = -1
            sensor_value["coordinate"] = self.car.position
            return sensor_value
        except ValueError:
            sensor_value["distance"] = -1
            sensor_value["coordinate"] = self.car.position
            return sensor_value

