from game_core.env import *
import pygame

class PygameView():
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.address = "GameView"

    def draw(self, data):
        '''
        called per frame, draw sprite on screen
        :param data: dictionary
        :return: None
        '''
        pass

    def draw_background(self):
        '''
        called per frame
        :return: None
        '''
        pass

    def flip(self):
        pygame.display.flip()

    def show_information(self):
        '''
        if want to show character on screen, this function will use pygame.font to draw
        :return: None
        '''
        pass