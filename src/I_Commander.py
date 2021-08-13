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

    {"TURN_LEFT": pygame.K_SPACE,
     "TURN_RIGHT": pygame.K_SPACE,
     "SPEED": pygame.K_SPACE,
     "BRAKE": pygame.K_SPACE},

    {"TURN_LEFT": pygame.K_SPACE,
     "TURN_RIGHT": pygame.K_SPACE,
     "SPEED": pygame.K_SPACE,
     "BRAKE": pygame.K_SPACE},

    {"TURN_LEFT": pygame.K_SPACE,
     "TURN_RIGHT": pygame.K_SPACE,
     "SPEED": pygame.K_SPACE,
     "BRAKE": pygame.K_SPACE},

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
        self.speed = 100

    def getControlDict(self):
        keys = pygame.key.get_pressed()
        control_list = [{"left_PWM": 0, "right_PWM": 0}]
        control_dic = {"LEFT": keys[self.moveLeftKey],
                       "RIGHT": keys[self.moveRightKey],
                       "SPEED_UP": keys[self.speedKey],
                       "BRAKEDOWN": keys[self.brakeKey]}

        if control_dic["SPEED_UP"]:
            control_list[0]["left_PWM"] = self.speed
            control_list[0]["right_PWM"] = self.speed
        elif control_dic["BRAKEDOWN"]:
            control_list[0]["left_PWM"] = -1 * self.speed
            control_list[0]["right_PWM"] = -1 * self.speed

        if control_dic["LEFT"]:
            control_list[0]["right_PWM"] += self.speed
            # control_list[0]["left_PWM"] -= self.speed
        elif control_dic["RIGHT"]:
            control_list[0]["left_PWM"] += self.speed

        return control_list
