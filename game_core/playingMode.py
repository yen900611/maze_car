from .gameMode import GameMode
from .env import *
import pygame
import random

class PlayingMode(GameMode):
    def __init__(self, user_num: int, sound_controller):
        super(PlayingMode, self).__init__()
        pygame.font.init()

        '''sound'''
        self.sound_controller = sound_controller

        '''image'''
        self.bg_image = pygame.image.load(path.join(IMAGE_DIR, BACKGROUND_IMAGE[0])).convert()

        self.cars_info = []
        self.sensor_value = []

    def update_sprite(self):
        '''update the model of game,call this fuction per frame'''
        self.frame += 1
        self.handle_event()

    def detect_collision(self):
        super(PlayingMode,self).detect_collision()
        pass

    def _print_result(self):
        pass

    def _init_world(self, user_no: int):
        pass

    def _init_maze(self):
        pass

    def _is_game_end(self):
        pass

    def _is_car_arrive_end(self, car):
        pass

    def draw_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(PlayingMode, self).draw_bg()
        pass

        '''畫出每台車子的資訊'''
        self._draw_user_imformation()

    def drawAllSprites(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(PlayingMode,self).drawAllSprites()
        pass

    def _draw_user_imformation(self):
        pass

    def rank(self):
        pass

