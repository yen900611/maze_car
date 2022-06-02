import pygame
from mlgame.game.paia_game import GameResultState, GameStatus
from .env import *


class Point(pygame.sprite.Sprite):
    def __init__(self, game, coordinate):
        self.group = game.all_points
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self.x, self.y = (coordinate[0] - TILESIZE / PPM, -coordinate[1] + TILESIZE / PPM)
        # self.x, self.y = (coordinate[0] + TILESIZE / (2 * PPM), -coordinate[1] - TILESIZE / (2 * PPM))

    def get_info(self):
        return {
            "coordinate": ((self.x + 0.5) * 5, (self.y - 0.5) * 5)
        }

    def get_progress_data(self):
        asset_data = {}
        return asset_data


class End_point(Point):
    def __init__(self, game, coordinate):
        Point.__init__(self, game, coordinate)
        self.rect = pygame.Rect(self.x, self.y, TILESIZE * 3, TILESIZE * 3)

    def update(self, *args, **kwargs) -> None:
        self.detect_cars_collision()

    def detect_cars_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.cars, False)
        for hit in hits:
            if hit.is_running:
                hit.end_frame = self.game.frame
                hit.is_completed = True
                self.game.eliminated_user.append(hit)  # TODO #外部注入
                self.game.state = GameResultState.FINISH
                hit.is_running = False
                hit.status = GameStatus.GAME_PASS

    def get_progress_data(self):
        asset_data = {"type": "image",
                      "x": self.rect.x,
                      "y": self.rect.y,
                      "width": 60,
                      "height": 60,
                      "image_id": "logo",
                      "angle": 0}
        return asset_data


class Check_point(Point):
    def __init__(self, game, coordinate):
        Point.__init__(self, game, coordinate)
        self.rect = pygame.Rect(self.x, self.y, TILESIZE * 3, TILESIZE * 3)
        self.car_has_hit = []

    def update(self, *args, **kwargs) -> None:
        self.detect_cars_collision()

    def detect_cars_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.cars, False)
        for hit in hits:
            if hit.status and hit not in self.car_has_hit:
                hit.check_point += 1
                self.car_has_hit.append(hit)

    def get_progress_data(self):
        asset_data = {"type": "rect",
                      "x": self.rect.x,
                      "y": self.rect.y,
                      "width": 60,
                      "height": 60,
                      "color": RED,
                      "angle": 0}
        return asset_data


class Outside_point(Point):
    '''
    if car colliding these point, car will be swich to start point
    '''

    def __init__(self, game, coordinate):
        Point.__init__(self, game, coordinate)
        # self.image = pygame.Surface((TILESIZE, TILESIZE))
        # self.image.fill(BLUE)
        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.x, self.y, TILESIZE * 3, TILESIZE * 3)

    def update(self, *args, **kwargs) -> None:
        self.detect_cars_collision()

    def detect_cars_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.cars, False)
        for hit in hits:
            if hit.status:
                hit.body.position = (hit.x, hit.y)
                hit.body.linearVelocity = 0, 0
                pass
