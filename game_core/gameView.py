import math

from .env import *
import pygame

class PygameView():
    def __init__(self, game_info:dict):
        pygame.display.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.address = "GameView"
        if "images" in game_info.keys():
            self.image_dict = self.loading_image(game_info["images"])

    def loading_image(self,dict):
        result = {}
        for file_name in dict:
            image = pygame.image.load(path.join(IMAGE_DIR, file_name))
            result[file_name]=image
            pass
        return result

    def draw(self, object_imformation):
        '''
        每個frame呼叫一次，把角色畫在螢幕上
        :param all_sprite:
        :return:
        '''
        object_imformation = self.check_game_object_information(object_imformation)
        for game_object in object_imformation["game_object"]:
            if game_object["type"] == "image":
                if "angle" in game_object.keys():
                    image = pygame.transform.rotate(pygame.transform.scale(self.image_dict[game_object["image"]], game_object["size"]), (game_object["angle"]* 180 / math.pi) % 360)
                    rect = image.get_rect()
                    rect.center = game_object["coordinate"]
                    self.screen.blit(image, rect)

                else:
                    self.screen.blit(pygame.transform.scale(self.image_dict[game_object["image"]], game_object["size"]), game_object["coordinate"])
            elif game_object["type"] == "rectangle":
                pygame.draw.rect(self.screen, game_object["color"],
                                 pygame.Rect(game_object["coordinate"], game_object["size"]))
                pass
            elif game_object["type"] == "vertices":
                pygame.draw.polygon(self.screen, game_object["color"], game_object["vertices"])
                pass
            else:
                pass
            pass

    def draw_screen(self):
        self.screen.fill(BLACK)
        pass

    def flip(self):
        pygame.display.flip()

    def draw_information(self, surf, text, size, x, y):
        font = pygame.font.Font(pygame.font.match_font("arial"), size)
        text_surface = font.render(text , True , WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surf.blit(text_surface , text_rect)

    def check_game_object_information(self, data: dict):
        object_information = data
        if "game_object" in object_information.keys():
            for game_object in object_information["game_object"]:
                if ("name" or "type" or "coordinate") not in game_object.keys():
                    object_information["game_object"].remove(game_object)
                else:
                    if game_object["type"] == "image":
                        if "image" not in game_object.keys():
                            object_information["game_object"].remove(game_object)
                    elif game_object["type"] == "rectangle":
                        if ("size" or "color") not in game_object.keys():
                            object_information["game_object"].remove(game_object)
                    elif game_object["type"] == "vertices":
                        if "vertices" not in game_object.keys():
                            object_information["game_object"].remove(game_object)
                    else:
                        object_information["game_object"].remove(game_object)
        # print(object_information)
        else:
            object_information["game_object"] = []

        return object_information