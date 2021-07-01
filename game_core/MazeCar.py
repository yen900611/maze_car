import math

from .mazeMode import MazeMode
from .moveMazeMode import MoveMazeMode
from .practiceMode import PracticeMode
from .sound_controller import *
from .gameView import PygameView
from .game_object_data import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class MazeCar:
    def __init__(self, user_num, game_type, map, time, sensor, sound):
        self.ranked_score = {"1P": 0, "2P": 0, "3P": 0, "4P": 0, "5P": 0, "6P": 0}  # 積分
        self.maze_id = map - 1
        self.game_end_time = time
        self.is_sound = sound
        if game_type == "MAZE":
            self.game_mode = MazeMode(user_num, map, time, sensor, self.is_sound)
            self.game_type = "MAZE"
        elif game_type == "MOVE_MAZE":
            self.game_mode = MoveMazeMode(user_num,map,time, sensor, self.is_sound)
            self.game_type = "MOVE_MAZE"

        elif game_type == "PRACTICE":
            self.game_mode = PracticeMode(user_num,map,time, sensor, self.is_sound)
            self.game_type = "PRACTICE"
        self.user_num = user_num
        self.game_mode.sound_controller.play_music()
        self.gameView = PygameView(self.get_game_info())

    def update(self, commands):
        self.game_mode.ticks()
        self.game_mode.handle_event()
        self.game_mode.update_sprite(commands)
        self.gameView.draw_screen()
        self.gameView.draw(self.get_game_progress())
        self.gameView.flip()
        # self.draw()
        if not self.isRunning():
            return "QUIT"

    def get_player_scene_info(self):
        scene_info = self.get_scene_info
        player_info = {}
        for car in self.game_mode.car_info:
            # type of car is dictionary
            player_info["ml_" + str(car["id"] + 1) + "P"] = {"frame": scene_info["frame"],
                                                             "status": scene_info["status"],
                                                             "x": car["coordinate"][0],
                                                             "y": car["coordinate"][1],
                                                             "angle": (car["angle"] * 180 / math.pi) % 360,
                                                             "R_sensor": car["r_sensor_value"]["distance"],
                                                             "L_sensor": car["l_sensor_value"]["distance"],
                                                             "F_sensor": car["f_sensor_value"]["distance"],
                                                             "L_T_sensor": car["l_t_sensor_value"]["distance"],
                                                             "R_T_sensor": car["r_t_sensor_value"]["distance"],
                                                             "end":self.game_mode.end_point.get_info()["coordinate"]}
        return player_info

    def reset(self):
        for key in self.game_mode.ranked_score.keys():
            self.ranked_score[key] += self.game_mode.ranked_score[key]
        print(self.ranked_score)
        # self.game_mode = PlayingMode(user_num, map, time, self.sound_controller)

    def isRunning(self):
        return self.game_mode.isRunning()

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
            scene_info[str(car["id"]) + "P_position"] = car["topleft"]
        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        game_info = get_scene_init_sample_data()
        game_info["map_width"] = self.game_mode.map.tileWidth * 20
        game_info["map_height"] =self.game_mode.map.tileHeight * 20
        return game_info

    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        game_progress = get_progress_data(self.game_mode)
        return game_progress

    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info
        result = self.game_mode.result
        rank = []
        for ranking in self.game_mode.ranked_user:
            same_rank = []
            for user in ranking:
                same_rank.append({"player":str(user.car_no+1)+"P",
                                  "game_result":str(user.end_frame) + "frames"})
            rank.append(same_rank)

        return {"frame_used": scene_info["frame"],
                # "result": result, # ["1P:7s", "2P:5s"]
                "ranks": rank# by score
                }

        pass

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        key_pressed_list = pygame.key.get_pressed()
        cmd_1P = [{"left_PWM": 0, "right_PWM": 0}]
        cmd_2P = [{"left_PWM": 0, "right_PWM": 0}]

        if key_pressed_list[pygame.K_UP]:
            cmd_1P[0]["left_PWM"] = 100
            cmd_1P[0]["right_PWM"] = 100
        if key_pressed_list[pygame.K_DOWN]:
            cmd_1P[0]["left_PWM"] = -100
            cmd_1P[0]["right_PWM"] = -100
        if key_pressed_list[pygame.K_LEFT]:
            cmd_1P[0]["right_PWM"] += 100
        if key_pressed_list[pygame.K_RIGHT]:
            cmd_1P[0]["left_PWM"] += 100

        if key_pressed_list[pygame.K_w]:
            cmd_2P[0]["left_PWM"] = 100
            cmd_2P[0]["right_PWM"] = 100
        if key_pressed_list[pygame.K_s]:
            cmd_2P[0]["left_PWM"] = -100
            cmd_2P[0]["right_PWM"] = -100
        if key_pressed_list[pygame.K_a]:
            cmd_2P[0]["right_PWM"] += 100
        if key_pressed_list[pygame.K_d]:
            cmd_2P[0]["left_PWM"] += 100

        return {"ml_1P": cmd_1P,
                "ml_2P": cmd_2P}
