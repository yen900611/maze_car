from game_test.mode_test import MazeMode
from game_core.env import *
from game_core.sound_controller import *
from game_core.gameView import PygameView

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class MazeCar:
    def __init__(self, user_num, game_type, map, time, sound):
        self.ranked_score = {"1P": 0, "2P": 0, "3P": 0, "4P": 0, "5P": 0, "6P": 0}  # 積分
        self.maze_id = map - 1
        self.game_end_time = time
        self.is_sound = sound
        self.sound_controller = SoundController(self.is_sound)
        if game_type == "MAZE":
            self.game_mode = MazeMode(user_num, map, time, self.sound_controller)
            self.game_type = "MAZE"
        elif game_type == "MOVE_MAZE":
            self.game_mode = MoveMazeMode(user_num,map,time, self.sound_controller)
            self.game_type = "MOVE_MAZE"
        self.user_num = user_num
        self.sound_controller.play_music()
        self.gameView = PygameView(self.get_game_info())

    def update(self, commands):
        self.game_mode.ticks()
        self.game_mode.handle_event()
        self.game_mode.detect_collision()
        self.game_mode.update_sprite(commands)
        game_object = self.get_game_progress()
        self.draw(game_object)
        if not self.isRunning():
            return "QUIT"

    def get_player_scene_info(self):
        scene_info = self.get_scene_info
        player_info = {}
        for car in self.game_mode.car_info:
            # type of car is dictionary
            player_info["ml_" + str(car["id"] + 1) + "P"] = {"frame": scene_info["frame"],
                                                             "status": scene_info["status"],
                                                             "R_sensor": car["r_sensor_value"],
                                                             "L_sensor": car["l_sensor_value"],
                                                             "F_sensor": car["f_sensor_value"], }
        return player_info

    def reset(self):
        for key in self.game_mode.ranked_score.keys():
            self.ranked_score[key] += self.game_mode.ranked_score[key]
        print(self.ranked_score)
        # self.game_mode = PlayingMode(user_num, map, time_to_play, self.sound_controller)

    def isRunning(self):
        return self.game_mode.isRunning()

    def draw(self, data):
        self.gameView.draw_screen()
        self.gameView.draw(data)
        self.gameView.flip()
        # self.game_mode.draw_bg()
        # self.game_mode.drawWorld()
        # self.game_mode.flip()

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
            scene_info[str(car["id"]) + "P_position"] = car["vertices"]
        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        wall_vertices = []
        if self.game_type == "MAZE":
            for wall in Normal_Maze_Map[self.maze_id]:
                vertices = []
                for vertice in wall:
                    vertices.append(
                        (vertice[0] * PPM * self.game_mode.size, HEIGHT - vertice[1] * PPM * self.game_mode.size))
                wall_vertices.append(vertices)
        elif self.game_type == "MOVE_MAZE":
            for wall in self.game_mode.walls:
                wall_vertices.append(wall.pixel_vertices)
        else:
            pass
        game_info = {
            "scene": {
                "size": [WIDTH, HEIGHT],
                "walls": wall_vertices  #pygame(pixel)
            },
            "game_object": [
                {"name": "player1_car", "size": self.game_mode.car.size, "color": RED, "image": "car0.png"},
                {"name": "player2_car", "size": self.game_mode.car.size, "color": GREEN, "image": "car_02.png"},
                {"name": "player3_car", "size": self.game_mode.car.size, "color": BLUE, "image": "car_03.png"},
                {"name": "player4_car", "size": self.game_mode.car.size, "color": YELLOW, "image": "car_04.png"},
                {"name": "player5_car", "size": self.game_mode.car.size, "color": BROWN, "image": "car_05.png"},
                {"name": "player6_car", "size": self.game_mode.car.size, "color": PINK, "image": "car_06.png"},
                {"name": "info", "size": (306, 480), "color": WHITE, "image": "info.png"},
            ],
            "images": ["car0.png", "car_02.png", "car_03.png", "car_04.png", "car_05.png", "car_06.png", "info.png",
                       ]
        }
        if self.game_type == "MOVE_MAZE":
            game_info["game_object"].append({"name": "wall", "size": (120,10), "color": WHITE})
        return game_info

    def _progress_dict(self, pos_left=None, pos_top=None, vertices=None, size=None, color=None, image=None, angle=None,
                       center=None):
        '''
        :return:Dictionary for game_progress
        '''
        object = {}
        if pos_left != None and pos_top != None:
            object["pos"] = [pos_left, pos_top]
        if vertices != None:
            object["vertices"] = vertices
        if size != None:
            object["size"] = size
        if color != None:
            object["color"] = color
        if image != None:
            object["image"] = image
        if angle != None:
            object["angle"] = angle
        if center != None:
            object["center"] = center

        return object

    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        game_info = {
            "scene": {
                "size": [WIDTH, HEIGHT],
                # "walls": wall_vertices  # pygame(pixel)
            },
            "game_object": [
                {"type": "image", "name": "info", "size": (306, 480), "color": WHITE, "image": "info.png",
                 "coordinate": (507, 20)},
            ],
            "images": ["car0.png", "car_02.png", "car_03.png", "car_04.png", "car_05.png", "car_06.png", "info.png",
                       ]
        }
        for user in self.game_mode.car_info:
            game_info["game_object"].append({"type": "image",
                                             "name": "player_car",
                                             "angle": user["angle"],
                                             "size": user["size"],
                                             "image": "car_0" + str(user["id"] + 1) + ".png",
                                             "coordinate": user["center"]})
        for wall in Normal_Maze_Map[self.maze_id]:
            vertices = []
            for vertice in wall:
                vertices.append(
                    (vertice[0] * PPM * self.game_mode.size, HEIGHT - vertice[1] * PPM * self.game_mode.size))
            game_info["game_object"].append({"type": "vertices",
                                             "name": "wall",
                                             "color": WHITE,
                                             "vertices": vertices})
        # print(game_info)

        return game_info

    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info
        result = self.game_mode.result

        return {"used_frame": scene_info["frame"],
                "result": result, # ["1P:7s", "2P:5s"]
                "rank": self.ranking()# by score
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

    def ranking(self):
        '''
        ranking by score
        :return: list
        [[],[],[],[],[],[]]
        '''
        ranked_player = []
        scores = []
        result = []
        for key in self.ranked_score.keys():
            scores.append(self.ranked_score[key])
            '''
            scores = [p1_score,p2_score....,p6_score]
            '''
        while len(scores) != 0:
            for key in self.ranked_score.keys():
                try:
                    if self.ranked_score[key] == max(scores):
                        ranked_player.append(key)
                        scores.remove(self.ranked_score[key])
                except ValueError:
                    pass
            '''
            ranked_player=[2P,3P,5P,1P,6P,4P] # sort from most score
            '''
        for i in range(len(ranked_player)):
            same_rank = []
            if i == len(ranked_player) - 1:
                same_rank.append(ranked_player[i])
                result.append(same_rank)
            elif self.ranked_score[ranked_player[i]] == self.ranked_score[ranked_player[i - 1]]:
                pass
            elif self.ranked_score[ranked_player[i]] == self.ranked_score[ranked_player[i + 1]]:
                same_rank.append(ranked_player[i])
                for j in range(1, len(ranked_player) - i):
                    if self.ranked_score[ranked_player[i + j]] == self.ranked_score[ranked_player[i]]:
                        if j == 0:
                            pass
                        else:
                            same_rank.append(ranked_player[i + j])
                            continue
                        break
                    else:
                        break
                result.append(same_rank)

            else:
                same_rank.append(ranked_player[i])
                result.append(same_rank)
        return result
