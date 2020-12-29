from .math_function import cross_point_dot
import math

from .sensor import Sensor
import pygame
from .env import *
import random


class Car():
    def __init__(self, world, position: tuple, car_no: int):
        self.car_no = car_no
        self.end_time = 0
        self.image = pygame.image.load(path.join(IMAGE_DIR, "car_0" + str(self.car_no + 1) + ".png"))
        self.status = True
        self.sensor_R = 0
        self.sensor_L = 0
        self.sensor_F = 0
        self.last_detect_sensor = 0
        self.velocity = 0
        self.body = world.CreateDynamicBody(position=position)
        self.box1 = self.body.CreatePolygonFixture(box=(0.9, 0.9), density=2, friction=0.1, restitution=0.3)
        self.vertices = []
        self.sensor_right = Sensor(world, (position[0] + 0.45, position[1]))
        self.sensor_left = Sensor(world, (position[0] - 0.45, position[1]))
        world.CreateDistanceJoint(bodyA=self.sensor_left.body, bodyB=self.body, collideConnected=True)
        world.CreateDistanceJoint(bodyA=self.sensor_right.body, bodyB=self.body, collideConnected=True)

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

    def detect_distance(self, frame):
        if frame - self.last_detect_sensor > FPS / 10:
            self.sensor_F = self.front_sensor_detect(wall_info)
            self.sensor_L = self.left_sensor_detect(wall_info)
            self.sensor_R = self.right_sensor_detect(wall_info)
            self.last_detect_sensor = frame
        pass

    def left_move(self, pwm: int):

        current_forward_normal = self.body.GetWorldVector((0, 1))

        if self.velocity > 0.01:
            f = self.body.GetWorldVector(localVector=(0.0, pwm / self.velocity))
        else:
            f = self.body.GetWorldVector(localVector=(0.0, pwm))

        # f = pwm*current_forward_normal
        p = self.body.GetWorldPoint(localPoint=(-1.0, 0.0))
        self.body.ApplyForce(f, p, True)

    def right_move(self, pwm: int):

        current_forward_normal = self.body.GetWorldVector((0, 1))

        if self.velocity > 0.01:
            f = self.body.GetWorldVector(localVector=(0.0, pwm / self.velocity))
        else:
            f = self.body.GetWorldVector(localVector=(0.0, pwm))

        # f = pwm*current_forward_normal

        p = self.body.GetWorldPoint(localPoint=(1.0, 0.0))
        self.body.ApplyForce(f, p, True)

    def keep_in_screen(self):
        pass

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "vertices": self.vertices,
                         "angle": (self.body.angle * 180 / math.pi) % 360,
                         "r_sensor_value": self.sensor_R,
                         "l_sensor_value": self.sensor_L,
                         "f_sensor_value": self.sensor_F,
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
                self.sensor_left.body.position[1] - self.sensor_right.body.position[1],
                self.sensor_right.body.position[0] - self.sensor_left.body.position[0])

        for wall in walls:
            distance.append(cross_point_dot(self.body.position,
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
            result = round(min(results) * 5, 1) + random.randint(0, 3)
            if result <0:
                result = 0
            return result
        except TypeError:
            return round(random.randrange(60.0), 1)
        except ValueError:
            return round(random.randrange(60.0), 1)

    def right_sensor_detect(self, walls):
        distance = []
        results = []
        dots = []
        for wall in walls:
            distance.append(cross_point_dot(self.sensor_right.body.position,
                                            self.sensor_left.body.position - self.sensor_right.body.position,
                                            wall[0], wall[1])
                            )
        for i in distance:
            if i:
                if self.sensor_left.body.position[0] > self.sensor_right.body.position[0] >= i[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_right.body.position[0]) ** 2 + (
                                    i[1] - self.sensor_right.body.position[1]) ** 2))
                elif i[0] >= self.sensor_right.body.position[0] > self.sensor_left.body.position[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_right.body.position[0]) ** 2 + (
                                    i[1] - self.sensor_right.body.position[1]) ** 2))
                else:
                    pass

        try:
            result = round(min(results) * 5, 1) + random.randint(0, 3)
            return result
        except TypeError:
            return round(random.randrange(60.0), 1)
        except ValueError:
            return round(random.randrange(60.0), 1)

    def left_sensor_detect(self, walls):
        distance = []
        results = []
        dots = []
        for wall in walls:
            distance.append(cross_point_dot(self.sensor_left.body.position,
                                            self.sensor_right.body.position - self.sensor_left.body.position,
                                            wall[0], wall[1])
                            )
        for i in distance:
            if i:
                if self.sensor_right.body.position[0] > self.sensor_left.body.position[0] >= i[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_left.body.position[0]) ** 2 + (
                                    i[1] - self.sensor_left.body.position[1]) ** 2))
                elif i[0] >= self.sensor_left.body.position[0] > self.sensor_right.body.position[0]:
                    dots.append(i)
                    results.append(
                        math.sqrt((i[0] - self.sensor_left.body.position[0]) ** 2 + (
                                    i[1] - self.sensor_left.body.position[1]) ** 2))
                else:
                    pass
        try:

            result = round(min(results) * 5, 1) + random.randint(0, 3)
            return result
        except TypeError:
            return round(random.randrange(60.0), 1)
        except ValueError:
            return round(random.randrange(60.0), 1)

    def get_polygon_vertice(self):
        self.vertices = [(self.body.transform * v) * PPM for v in self.box1.shape.vertices]
        self.vertices = [(v[0], HEIGHT - v[1]) for v in self.vertices]
        pass
