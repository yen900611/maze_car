import random
from .env import *


class Scene():
    def __init__(self, width: int, height: int, color: str = "#000000"):
        """
        This is a value object
        :param width:
        :param height:
        :param color:
        :param image:
        """
        self.width = width
        self.height = height
        self.color = color


def get_progress_data(game_mode):
    game_progress = {
        "background": [],
        "object_list": [],
        "toggle": [],
        "foreground": [],
        "user_info": [],
        "game_sys_info": {}
    }

    for car in game_mode.car_info:
        if car["id"] % 2 == 0:
            x = 600
        else:
            x = 730

        if car["status"]:
            game_progress["background"].append(
                get_dummy_text("L:" + str(car["l_sensor_value"]["distance"]) + "cm", "#FFFF00", (x,
                                                                                                 178 + 20 + 94 * (car[
                                                                                                                      "id"] // 2)),
                               "15px Arial"))
            game_progress["background"].append(
                get_dummy_text("F:" + str(car["f_sensor_value"]["distance"]) + "cm", "#FF0000", (x,
                                                                                                 178 + 40 + 94 * (car[
                                                                                                                      "id"] // 2)),
                               "15px Arial"))
            game_progress["background"].append(
                get_dummy_text("R:" + str(car["r_sensor_value"]["distance"]) + "cm", "#21A1F1", (x,
                                                                                                 178 + 60 + 94 * (car[
                                                                                                                      "id"] // 2)),
                               "15px Arial"))
            game_progress["object_list"].append(get_line_object("l_sensor", car["center"],
                                                                trnsfer_box2d_to_pygame(game_mode,
                                                                                        car["l_sensor_value"][
                                                                                            "coordinate"]), "#FFFF00",
                                                                5))

            game_progress["object_list"].append(get_line_object("l_top_sensor", car["center"],
                                                                trnsfer_box2d_to_pygame(game_mode,
                                                                                        car["l_t_sensor_value"][
                                                                                            "coordinate"]), "#FFFF00",
                                                                5))

            game_progress["object_list"].append(get_line_object("r_top_sensor", car["center"],
                                                                trnsfer_box2d_to_pygame(game_mode,
                                                                                        car["r_t_sensor_value"][
                                                                                            "coordinate"]), "#21A1F1",
                                                                5))
            game_progress["object_list"].append(get_line_object("r_sensor", car["center"],
                                                                trnsfer_box2d_to_pygame(game_mode,
                                                                                        car["r_sensor_value"][
                                                                                            "coordinate"]), "#21A1F1",
                                                                5))
            game_progress["object_list"].append(get_line_object("f_sensor", car["center"],
                                                                trnsfer_box2d_to_pygame(game_mode,
                                                                                        car["f_sensor_value"][
                                                                                            "coordinate"]), "#FF0000",
                                                                5))
        else:
            game_progress["background"].append(get_dummy_text(str(car["end_frame"]) + "frame", "#FFFFFF",
                                                              (x, 178 + 40 + 94 * (car["id"] // 2)), "15px Arial"))
    # try:
    #     for car in game_mode.car_info:
    #         game_progress["object_list"].append(
    #             get_image_object("car_0"+str(car["id"]+1), (car["topleft"][0], car["topleft"][1]), 50, 40, car["angle"])
    #         )
    # except Exception:
    #     pass
    for user in game_mode.car_info:
        game_progress["user_info"].append({
            "player": str(user["id"] + 1) + "P",
            "F_sensor": user["f_sensor_value"]["distance"],
            "R_sensor": user["r_sensor_value"]["distance"],
            "L_sensor": user["l_sensor_value"]["distance"],
            "R_PWM": user["R_PWM"],
            "L_PWM": user["L_PWM"],
        })

    game_progress["game_sys_info"]["frame"] = game_mode.frame
    return game_progress


def get_scene_init_sample_data() -> dict:
    """
    :rtype: dict
    :return:  遊戲場景初始化的資料
    """

    scene = Scene(WIDTH, HEIGHT)
    assets = [
        {
            "type": "image",
            "image_id": 'car_01',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_01.png'
        }, {
            "type": "image",
            "image_id": 'car_02',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_02.png'
        }, {
            "type": "image",
            "image_id": 'car_03',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_03.png'
        }, {
            "type": "image",
            "image_id": 'car_04',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_04.png'
        }, {
            "type": "image",
            "image_id": 'car_05',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_05.png'
        }, {
            "type": "image",
            "image_id": 'car_06',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_06.png'
        }, {
            "type": "image",
            "image_id": 'info',
            "width": 306,
            "height": 480,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/info.png'
        }, {
            "type": "image",
            "image_id": 'logo',
            "width": 40,
            "height": 40,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/logo.png'
        }
    ]
    return {"scene": scene.__dict__,
            "assets": assets,
            # "audios": {}
            }


def get_image_object(image_id, coordinate, width, height, angle=0):
    """
    這是一個用來繪製圖片的資料格式，
    "type"表示不同的類型
    "x" "y" 表示物體左上角的座標
    "width" "height"表示其大小
    "image_id"表示其圖片的識別號，需在
    "angle"表示其順時針旋轉的角度
    """
    return {"type": "image",
            "x": coordinate[0],
            "y": coordinate[1],
            "width": width,
            "height": height,
            "image_id": image_id,
            "angle": int(angle)}


def get_rect_object(name, coordinate, width, height, color, angle=0):
    """
    這是一個用來繪製矩形的資料格式，
    "type"表示不同的類型
    "x""y"表示其位置，位置表示物體左上角的座標
    "size"表示其大小
    "image"表示其圖片
    "angle"表示其順時針旋轉的角度
    "color"以字串表示
    :return:
    """
    return {"type": "rect",
            "name": name,
            "x": coordinate[0],
            "y": coordinate[1],
            "angle": int(angle),
            "width": width,
            "height": height,
            "color": color
            }


def get_line_object(name, dot1, dot2, color, width=2):
    """
    這是一個用來繪製矩形的資料格式，
    "type"表示不同的類型
    "x""y"表示其位置，位置表示物體左上角的座標
    "size"表示其大小
    "image"表示其圖片
    "angle"表示其順時針旋轉的角度
    "color"以字串表示
    :return:
    """
    return {"type": "line",
            "name": name,
            "x1": int(dot1[0]),
            "y1": int(dot1[1]),
            "x2": int(dot2[0]),
            "y2": int(dot2[1]),
            "width": width,
            "color": color
            }


def get_polygon_object(name, points, color):
    """
    這是一個用來繪製多邊形的資料格式，
    points欄位至少三個 # [{"x":1,"y":2},{},{}]
    :return:dict
    """
    vertices = []
    for p in points:
        vertices.append({"x": p[0], "y": p[1]})
    return {"type": "polygon",
            "name": name,
            "color": color,
            "points": vertices
            }


def get_dummy_text(content, color, coordinate, font_style="24px Arial"):
    return {
        "type": "text",
        "content": content,
        "color": color,
        "x": coordinate[0],
        "y": coordinate[1],
        "font-style": font_style
    }


def get_dummy_progress_data():
    pass
    # return {"game_object_list":
    #             [get_dummy_polygon(), get_dummy_image(),
    #              get_dummy_rect(), get_dummy_text()],
    #         "game_user_info":
    #             [{"player": "1P",
    #               "key": "value"
    #               }, {}, {}],
    #         "game_sys_info": {}
    #         }


def get_dummy_result_data():
    return {
        "frame_used": 15,
        "ranks": [
            [  # 1st
                {"player": "1P",  # 給系統mapping
                 "game_result": "7s",  # 顯示給玩家的
                 # 可自行增加
                 },
                {"player": "1P",  # 給系統mapping
                 "game_result": "7s",  # 顯示給玩家的
                 # 可自行增加
                 }
            ],
            [  # 2nd

            ],
            [  # 3rd

            ]
            #     player
        ],

    }


def gen_points(point_num: int = 4) -> list:
    result = []
    for i in range(point_num):
        result.append({"x": random.randint(0, 100), "y": random.randint(0, 100)})
    return result


def gen_rects(rect_num: int = 1) -> list:
    result = []
    for i in range(rect_num):
        result.append(gen_points(4))
    return result


def trnsfer_box2d_to_pygame(game, coordinate):
    '''
    :param coordinate: vertice of body of box2d object
    :return: center of pygame rect
    '''
    return ((coordinate[0] - game.pygame_point[0]) * PPM, (game.pygame_point[1] - coordinate[1]) * PPM)
