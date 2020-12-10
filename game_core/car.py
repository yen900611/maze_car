import pygame
import Box2D
import time
from .env import *
import random

class Car():
    def __init__(self,):
        pass

    def speedUp(self):
        pass

    def brakeDown(self):
        pass

    def moveRight(self):
        pass

    def moveLeft(self):
        pass

    def keep_in_screen(self):
        pass

    def get_info(self):

        self.car_info = {"id": self.car_no,
                         "pos": (self.rect.left, self.rect.top),
                         "distance": self.distance,
                         "velocity": self.velocity,
                         "coin_num": self.coin_num}
        return self.car_info
