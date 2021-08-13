import time

import pygame
from .env import *

class Point(pygame.sprite.Sprite):
    def __init__(self,game, coordinate):
        self.group = game.all_points
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self.x, self.y = (coordinate[0] + TILESIZE / (2 * PPM), -coordinate[1] - TILESIZE / (2 * PPM))

    def get_info(self):
        return {
            "coordinate":(self.x, self.y)
        }

class End_point(Point):
    def __init__(self, game, coordinate):
        Point.__init__(self, game, coordinate)
        self.image = pygame.Surface( (TILESIZE*2, TILESIZE* 2))
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs) -> None:
        self.detect_cars_collision()

    def detect_cars_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.cars, False)
        for hit in hits:
            if hit.status:
                hit.end_frame = self.game.frame
                hit.is_completed = True
                self.game.eliminated_user.append(hit)
                hit.is_running = False
                hit.status = "GAME_PASS"

class Check_point(Point):
    def __init__(self, game, coordinate):
        Point.__init__(self, game, coordinate)
        self.image = pygame.Surface((TILESIZE*2, TILESIZE*2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.car_has_hit = []

    def update(self, *args, **kwargs) -> None:
        self.detect_cars_collision()

    def detect_cars_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.cars, False)
        for hit in hits:
            if hit.status and hit not in self.car_has_hit:
                hit.check_point += 1
                self.car_has_hit.append(hit)

class Outside_point(Point):
    '''
    if car colliding these point, car will be swich to start point
    '''
    def __init__(self, game, coordinate):
        Point.__init__(self, game, coordinate)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs) -> None:
        self.detect_cars_collision()

    def detect_cars_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.cars, False)
        for hit in hits:
            if hit.status:

                hit.body.position = (hit.x, hit.y)
                hit.body.linearVelocity = 0, 0
                pass

