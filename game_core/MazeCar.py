import pygame
from .playingMode import PlayingMode
from .env import *
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class MazeCar:
    def __init__(self, user_num,game_type, level,sound):
        self.maze_id = level-1
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
            player_info["ml_"+str(car["id"]+1)+"P"] ={"R_sensor":car["r_sensor_value"],
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
        }
        for car in self.game_mode.car_info:
            # type of car is dictionary
            scene_info[str(car[id])+"P_position"] = car[vertices]
        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        wall_vertices = []
        for wall in Maze[self.maze_id]:
            vertices = []
            for vertice in wall:
                vertices.append((vertice[0]*PPM, HEIGHT - vertice[1]*PPM))
            wall_vertices.append(vertices)
        game_info = {
            "scene": {
                "size": [WIDTH, HEIGHT],
                "walls": wall_vertices #
            },
            "game_object": [
                {"name": "player1_car", "size": 36, "color": RED, "image": "car01.png"},
                {"name": "player2_car", "size": 36, "color": GREEN, "image": "car02.png"},
                {"name": "player3_car", "size": 36, "color": BLUE, "image": "car03.png"},
                {"name": "player4_car", "size": 36, "color": YELLOW, "image": "car04.png"},
                {"name": "player5_car", "size": 36, "color": BROWN, "image": "car05.png"},
                {"name": "player6_car", "size": 36, "color": PINK, "image": "car06.png"},
                {"name": "info", "size": (306, 480), "color": WHITE, "image": "info.png"},
            ],
            "images": ["car01.png", "car02.png", "car03.png", "car04.png", "car05.png", "car06.png","info.png",
                      ]
        }
        return game_info

    def _progress_dict(self, pos_left = None, pos_top = None,vertices = None, size = None, color = None, image = None, angle = None):
        '''
        :return:Dictionary for game_progress
        '''
        object = {}
        if pos_left !=None and pos_top !=None:
            object["pos"] = [pos_left, pos_top]
        if vertices !=None:
            object["vertices"] = vertices
        if size != None:
            object["size"] = size
        if color != None:
            object["color"] = color
        if image != None:
            object["image"] = image
        if angle != None:
            object["angle"] = angle

        return object

    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        scene_info = self.get_scene_info
        game_progress = {"game_object": {
            "info": [self._progress_dict(507, 20)],}}
        for user in self.game_mode.car_info:
            game_progress["player" + str(user["id"]+1)+"_car"]:[self._progress_dict(vertices=user["vertices"], angle=user["angle"])]
        return game_progress

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
        cmd_1P = [{"left_PWM" : 0, "right_PWM" : 0}]
        cmd_2P = [{"left_PWM" : 0, "right_PWM" : 0}]

        if key_pressed_list[pygame.K_UP]:
            cmd_1P[0]["left_PWM"] = 75
            cmd_1P[0]["right_PWM"] = 75
        if key_pressed_list[pygame.K_DOWN]:
            cmd_1P[0]["left_PWM"] = -75
            cmd_1P[0]["right_PWM"] = -75
        if key_pressed_list[pygame.K_LEFT]:
            cmd_1P[0]["right_PWM"] += 75
        if key_pressed_list[pygame.K_RIGHT]:
            cmd[0]["left_PWM"] += 75

        if key_pressed_list[pygame.K_w]:
            cmd_2P[0]["left_PWM"] = 75
            cmd_2P[0]["right_PWM"] = 75
        if key_pressed_list[pygame.K_s]:
            cmd_2P[0]["left_PWM"] = -75
            cmd_2P[0]["right_PWM"] = -75
        if key_pressed_list[pygame.K_a]:
            cmd_2P[0]["right_PWM"] += 75
        if key_pressed_list[pygame.K_d]:
            cmd_2P[0]["left_PWM"] += 75

        return {"ml_1P":cmd_1P,
                "ml_2P":cmd_2P}

# if __name__ == "__main__":
#     game=MazeCar(1,"NORMAL",1,"off")
#     print(game.get_game_progress())
