"""
This is a base class for different mode in game.
"""
import pygame
from .env import *

class GameMode(object):
    def __init__(self, pygame_screen=pygame.display.set_mode((WIDTH, HEIGHT)), bg_img=pygame.Surface((WIDTH, HEIGHT))):
        self.screen = pygame_screen
        self.bg_img = bg_img
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame = 0

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

    def update_sprite(self):
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

    def draw_information(self):
        pass

    def cross_point(self, dot1, vec1, dot2, vec2):
        '''
        define line A and line B, write a function which can return the point two lines cross.
        dot_1 = (x1, y1)
        dot_2 = (x2, y2)
        vec_1 = (vx1, vy1)
        vec_2 = (vx2, vy2)
        line1 = [(x1, y1), (x1 + vx1, y1 + vy1)], line2 = [(x2, y2), (x2 + vx2, y2 + vy2)]
        '''
        x1 = dot1[0]
        y1 = dot1[1]
        x2 = dot2[0]
        y2 = dot2[1]
        vx1 = vec1[0]
        vy1 = vec1[1]
        vx2 = vec2[0]
        vy2 = vec2[1]
        if vx1 == 0:  # 如果斜率為0
            k1 = None
            b1 = 0
        else:
            k1 = vy1 * 1.0 / vx1
            b1 = (y1 + vy1) * 1.0 - (x1 + vx1) * k1 * 1.0
        if vx2 == 0:
            k2 = None
            b2 = 0
        else:
            k2 = vy2 * 1.0 / vx2
            b2 = (y2 + vy2) * 1.0 - (x2 + vx2) * k2 * 1.0

        if k1 == k2:
            return None
        elif k1 == None:  # 如果Line1斜率不存在，則取Line1上的點帶入Line2的公式
            x = x1 + vx1
            k1 = k2
            b1 = b2
        elif k2 == None:
            x = x2 + vx2
        else:
            x = (b2 - b1) * 1.0 / (k1 - k2)
        y = k1 * x * 1.0 + b1 * 1.0
        return (x, y)

    def cross_point_dot(self, dot1, vec1, dot2, dot3):
        '''
        this function is same as above. But in this case, one of lines has starting point and ending point.
        If the point two line cross out of the line, function should return None.
        '''
        x2 = dot2[0]
        y2 = dot2[1]
        x3 = dot3[0]
        y3 = dot3[1]
        p = cross_point(dot1, vec1, dot2, (x3 - x2, y3 - y2))
        if p:
            if x2 <= p[0] <= x3 or x3 <= p[0] <= x2:
                if y2 <= p[1] <= y3 or y3 <= p[1] <= y2:
                    return p
                else:
                    return None
        else:
            return None
