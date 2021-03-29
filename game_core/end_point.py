import time

import pygame
from game_core.env import *

class End_point(pygame.sprite.Sprite):
    def __init__(self, game, coordinate):
        self.group = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self.image = pygame.image.load(path.join(IMAGE_DIR, LOGO))
        self.image = pygame.transform.scale(self.image, (TILESIZE*2, TILESIZE* 2))
        # self.image = pygame.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x, self.y = coordinate
        self.rect.x, self.rect.y = self.x * TILESIZE, self.y * TILESIZE
        pass

    def update(self, *args, **kwargs) -> None:
        self.detect_cars_collision()

    def detect_cars_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.cars, False)
        for hit in hits:
            if hit.status:
                hit.end_time = round(time.time() - self.game.start_time)
                self.game.eliminated_user.append(hit)
                self.game.user_time.append(hit.end_time)
                hit.status = False
        pass
