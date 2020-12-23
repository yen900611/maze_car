import pygame
from os import path
from .env import *

class SoundController():
    def __init__(self, is_sound_on):
        if is_sound_on == "on":
            self.is_sound_on = True
            pygame.mixer.init()
            pygame.mixer.music.set_volume(0.4)
        else:
            self.is_sound_on = False

    def play_music(self):
        pass
        # if self.is_sound_on:
        #     pygame.mixer.music.play(-1)
        # else:
        #     pass