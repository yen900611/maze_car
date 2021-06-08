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


    def rank(self):
        completed_game_user = []
        unfinish_game_user = []
        user_end_frame = []
        user_check_point = []
        for car in self.eliminated_user:
            if car.is_completed:
                user_end_frame.append(car.end_frame)
                completed_game_user.append(car)
            else:
                user_check_point.append(car.check_point)
                unfinish_game_user.append(car)
        same_rank = []
        rank_user = [] # [[sprite, sprite],[]]

        result = [user_end_frame.index(x) for x in sorted(user_end_frame)]
        for i in range(len(result)):
            if result[i] != result[i-1] or i == 0:
                if same_rank:
                    rank_user.append(same_rank)
                same_rank = []
                same_rank.append(completed_game_user[result[i]])
            else:
                for user in completed_game_user:
                    if user.end_frame == same_rank[0].end_frame and user not in same_rank:
                        same_rank.append(user)
                    else:
                        pass
        if same_rank:
            rank_user.append(same_rank)

        same_rank = []
        result = [user_check_point.index(x) for x in sorted(user_check_point, reverse=True)]
        for i in range(len(result)):
            if result[i] != result[i-1] or i == 0:
                if same_rank:
                    rank_user.append(same_rank)
                same_rank = []
                same_rank.append(unfinish_game_user[result[i]])
            else:
                for user in unfinish_game_user:
                    if user.check_point == same_rank[0].check_point and user not in same_rank:
                        same_rank.append(user)
                    else:
                        pass
        if same_rank:
            rank_user.append(same_rank)
        return rank_user

    def trnsfer_box2d_to_pygame(self, coordinate):
        '''
        :param coordinate: vertice of body of box2d object
        :return: center of pygame rect
        '''
        return ((coordinate[0]- self.pygame_point[0]) * PPM, (self.pygame_point[1] - coordinate[1])*PPM)