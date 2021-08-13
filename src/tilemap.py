import json

import pygame
from .env import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename) as json_file:
            data = json.load(json_file)
            self.tileHeight = data["height"]
            self.tileWidth = data["width"]
            map = []
            for i in range(self.tileHeight):
                self.data.append(data["layers"][0]["data"][i * self.tileWidth:(i + 1) * self.tileWidth])
        # with open(filename,'rt') as f:
        #     for line in f:
        #         data = []
        #         line.strip() # ignore"\n"
        #         for c in line:
        #             data.append(c)
        #         self.data.append(data)
        # self.tileWidth = len(self.data[0])
        # self.tileHeight = len(self.data)
        self.width = self.tileWidth * TILESIZE
        self.height = self.tileHeight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0,x)
        x = max(-(self.width - WIDTH+1), x)
        y = min(0,y)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)