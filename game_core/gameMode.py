"""
This is a base class for different mode in game.
"""
import math
import time

import pygame
from .env import *

class GameMode(object):
    def __init__(self, pygame_screen=pygame.display.set_mode((WIDTH, HEIGHT)), bg_img=pygame.Surface((WIDTH, HEIGHT))):
        self.screen = pygame_screen
        self.bg_img = bg_img
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame = 0
        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.match_font("arial", bold=True), 15)
        self.time_font = pygame.font.Font(pygame.font.match_font("arial", bold=True), 46)
        self.start_time = time.time()

    def ticks(self, fps=FPS):
        """This method should be called once per frame.
        It will compute how many milliseconds have passed since the previous call.
        :param fps: frame per second 每秒的繪圖次數
        :return: None
        """
        self.clock.tick(fps)

    def handle_event(self):
        """ Handle the event from window , mouse or button.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def detect_collision(self):
        """ Detect the collision event between sprites.
        :return: None
        """
        pass

    def update_sprite(self, *args):
        """ This function should update every sprite in games.
        :return: None
        """
        pass

    def draw_bg(self):
        """  Draw a background on screen.
        :return:None
        """
        pass

    def drawWorld(self):
        """  This function should draw every sprite on specific surface.
        :return: None
        """
        pass

    def flip(self):
        """Update the full display Surface to the screen
        :return:None
        """
        pygame.display.flip()

    def isRunning(self) -> bool:
        return self.running

    def draw_time(self,present_frame):
        now_time = present_frame / FPS
        min = round(now_time // 60)
        if min//10 <1:
            min_str = "0"+str(min)
        else:
            min_str = str(min)
        sec = math.floor(now_time)%60
        if sec//10 <1:
            sec_str = "0"+str(sec)
        else:
            sec_str = str(sec)
        ms = round(round(now_time - math.floor(now_time), 2)*100)
        if ms//10 <1:
            ms_str = "0"+str(ms)
        else:
            ms_str = str(ms)
        text_surface = self.time_font.render(min_str+" : "+sec_str+" : "+ms_str, True , WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center= (660, 100)
        self.screen.blit(text_surface , text_rect)

    def draw_information(self, surf, color, text, x, y):
        text_surface = self.font.render(text , True , color)
        text_rect = text_surface.get_rect()
        text_rect.left,text_rect.top = (x, y)
        surf.blit(text_surface , text_rect)

