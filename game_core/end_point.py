import pygame

class End_point(pygame.sprite.Sprite):
    def __init__(self, game, coordinate):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.surface = pygame.Surface((120*self.game.size, 120*self.game.size))
        self.rect = self.surface.get_rect()
        self.rect.center = coordinate
        pass

    def detect_cars_collision(self):
        pass
