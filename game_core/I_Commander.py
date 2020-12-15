import abc
import pygame

class I_Commander(abc.ABC):
    @abc.abstractmethod
    def getControlDict(self) -> dict:
        pass

keyboardSet = [
    {"TURN_LEFT": pygame.K_LEFT,
     "TURN_RIGHT": pygame.K_RIGHT,
     "SPEED": pygame.K_UP,
     "BRAKE": pygame.K_DOWN},

    {"TURN_LEFT": pygame.K_a,
     "TURN_RIGHT": pygame.K_d,
     "SPEED": pygame.K_w,
     "BRAKE": pygame.K_s},

    {"TURN_LEFT": pygame.K_SPACE,
     "TURN_RIGHT": pygame.K_SPACE,
     "SPEED": pygame.K_SPACE,
     "BRAKE": pygame.K_SPACE},

    {"TURN_LEFT": pygame.K_SPACE,
     "TURN_RIGHT": pygame.K_SPACE,
     "SPEED": pygame.K_SPACE,
     "BRAKE": pygame.K_SPACE}

]

class KeyBoardCommander(I_Commander):
    def __init__(self, keyboard_no=0):
        self.no = keyboard_no
        self.speedKey = keyboardSet[keyboard_no]["SPEED"]
        self.brakeKey = keyboardSet[keyboard_no]["BRAKE"]
        self.moveLeftKey = keyboardSet[keyboard_no]["TURN_LEFT"]
        self.moveRightKey = keyboardSet[keyboard_no]["TURN_RIGHT"]

    def getControlDict(self):
        keys = pygame.key.get_pressed()
        control_list = []
        control_dic = {"LEFT": keys[self.moveLeftKey],
                       "RIGHT": keys[self.moveRightKey],
                       "SPEED_UP": keys[self.speedKey],
                       "BRAKEDOWN": keys[self.brakeKey]}
        if control_dic["LEFT"]:
            control_list.append("TURN_LEFT")
        if control_dic["RIGHT"]:
            control_list.append("TURN_RIGHT")
        if control_dic["SPEED_UP"]:
            control_list.append("SPEED")
        if control_dic["BRAKEDOWN"]:
            control_list.append("BRAKE")

        return control_list

