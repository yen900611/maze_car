import random
from .env import *

class Scene():
    def __init__(self, width: int, height: int, color: str = "#e3f2fdFF"):
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
        pass

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
            "url": 'https://github.com/yen900611/Maze_Car/blob/master/game_core/image/info.png'
        }, {
            "type": "image",
            "image_id": 'logo',
            "width": 40,
            "height": 40,
            "url": 'https://github.com/yen900611/Maze_Car/blob/master/game_core/image/logo.png'
        }
    ]
    return {"scene": scene.__dict__,
            "assets": assets,
            # "audios": {}
            }

def get_image_object(image_id, coordinate, width, height, angle = 0):
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
            "angle": angle}

def get_rect_object(name, coordinate, width, height, color, angle = 0):
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
            "angle": angle,
            "width": width,
            "height": height,
            "color": color
            }

def get_polygon_object(name, points, color):
    """
    這是一個用來繪製多邊形的資料格式，
    points欄位至少三個 # [{"x":1,"y":2},{},{}]
    :return:dict
    """
    return {"type": "polygon",
            "name": name,
            "color": color,
            "points": points
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
