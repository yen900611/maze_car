import math

from os import path
# from .game_object_data import *
import pygame

from .env import IMAGE_DIR

NAME = "name"
TYPE = "type"
ANGLE = "angle"
SIZE = "size"
COLOR = "color"
CORDINATE = "coordinate"
IMAGE = "image"
RECTANGLE = "rect"
POLYGON = "polygon"

class PygameView():
    def __init__(self, game_info:dict):
        pygame.display.init()
        self.scene_init_data = game_info
        self.width = self.scene_init_data["scene"]["width"]
        self.height = self.scene_init_data["scene"]["height"]
        self.background_color = self.scene_init_data["scene"]["color"]
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.address = "GameView"
        self.image_dict = self.loading_image()
        # if "images" in game_info.keys():
        #     self.image_dict = self.loading_image(game_info["images"])

    def loading_image(self):
        result = {}
        for file in self.scene_init_data["assets"]:
            if file[TYPE] == IMAGE:
                image = pygame.image.load(path.join(IMAGE_DIR, file["image_id"]+".png"))
                result[file["image_id"]]=image
        return result

    def draw(self, object_imformation):
        '''
        每個frame呼叫一次，把角色畫在螢幕上
        :param all_sprite:
        :return:
        '''
        self.draw_screen()
        for game_object in object_imformation["game_object_list"]:
            if game_object[TYPE] == IMAGE:
                self.draw_image(game_object["image_id"], game_object["x"], game_object["y"],
                                game_object["width"], game_object["height"], game_object["angle"])

            elif game_object[TYPE] == RECTANGLE:
                self.draw_rect(game_object["x"], game_object["y"], game_object["width"], game_object["height"],
                               game_object[COLOR])

            elif game_object[TYPE] == POLYGON:
                self.draw_polygon(game_object["points"], game_object[COLOR])

            elif game_object[TYPE] == "text":
                self.draw_text(game_object["content"], game_object["font-style"],
                               game_object["x"], game_object["y"], game_object[COLOR])

            else:
                pass


    def draw_screen(self):
        self.screen.fill(self.background_color) # hex # need turn to RGB

    def draw_image(self, image_id, x, y, width, height, angle):
        image = pygame.transform.rotate(pygame.transform.scale(self.image_dict[image_id], (width, height)),
                                        (angle * 180 / math.pi) % 360)
        rect = image.get_rect()
        rect.x, rect.y = x, y
        self.screen.blit(image, rect)

    def draw_rect(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))

    def draw_polygon(self, points, color):
        vertices = []
        for p in points:
            vertices.append((p["x"], p["y"]))
        pygame.draw.polygon(self.screen, color, vertices)

    def flip(self):
        pygame.display.flip()

    def draw_text(self, text, font_style, x, y, color):
        list = font_style.split(" ", -1)
        size = int(list[0].replace("px", "", 1))
        font_type = list[1].lower()
        font = pygame.font.Font(pygame.font.match_font(font_type), size)
        text_surface = font.render(text , True , color)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = (x, y)
        self.screen.blit(text_surface , text_rect)
