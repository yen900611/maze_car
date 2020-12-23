import pygame
from .playingMode import PlayingMode
from .env import *
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class MazeCar:
    def __init__(self, user_num,game_type, level,sound):
        self.maze_id = level
        self.is_sound = sound
        self.sound_controller = SoundController(self.is_sound)
        self.game_mode = PlayingMode(user_num,self.sound_controller)
        self.game_type = "NORMAL"
        self.user_num = user_num

    def get_player_scene_info(self):
        scene_info = self.get_scene_info
        player_info = {}
        for car in self.game_mode.car_info:
            # type of car is dictionary
            player_info[str(car[id])+"P"] = {"R_sensor":car["r_sensor_value"],
                                             "L_sensor":car["l_sensor_value"],
                                             "F_sensor":car["f_sensor_value"],}
        return player_info
    def update(self, commands):
        self.game_mode.handle_event()
        self.game_mode.detect_collision()
        self.game_mode.update_sprite(commands)
        self.draw()
        if not self.isRunning():
            return "QUIT"

    def reset(self):
        self.__init__(self.user_num,self.game_type,self.maze_id,self.is_sound)

    def isRunning(self):
        return self.game_mode.isRunning()

    def draw(self):
        self.game_mode.draw_bg()
        self.game_mode.drawWorld()
        self.game_mode.flip()

    @property
    def get_scene_info(self):
        """
        Get the scene information
        """
        scene_info = {
            "frame": self.game_mode.frame,
            "status": self.game_mode.status,
            "maze":Maze[self.maze_id]
        }
        for car in self.game_mode.car_info:
            # type of car is dictionary
            scene_info[str(car[id])+"P_position"] = car[vertices]
        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        pass

    def _progress_dict(self, pos_left, pos_top, size = None, color = None, image = None):
        '''
        :return:Dictionary for game_progress
        '''
        object = {"pos" : [pos_left, pos_top]}
        if size != None:
            object["size"] = size
        if color != None:
            object["color"] = color
        if image != None:
            object["image"] = image

        return object

    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        pass

    def get_game_result(self):
        """
        Get the game result for the web
        """
        pass

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        key_pressed_list = pygame.key.get_pressed()
        cmd_1P = []
        cmd_2P = []

        if key_pressed_list[pygame.K_DOWN]: cmd_1P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_UP]:cmd_1P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_LEFT]:cmd_1P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_RIGHT]:cmd_1P.append(RIGHT_cmd)

        if key_pressed_list[pygame.K_s]: cmd_2P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_w]:cmd_2P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_a]:cmd_2P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_d]:cmd_2P.append(RIGHT_cmd)

        return {"ml_1P":cmd_1P,
                "ml_2P":cmd_2P}
