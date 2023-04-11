from os import path

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS

'''width and height'''
WIDTH = 860
HEIGHT = 560
TILE_WIDTH = 540  # 大小
TILE_HEIGHT = 540

'''tile-base'''
TILESIZE = 20
TILE_LEFTTOP = 20, 20  # pixel
GRIDWIDTH = (TILE_WIDTH + TILE_LEFTTOP[0]) / TILESIZE
GRIDHEIGHT = (TILE_HEIGHT + TILE_LEFTTOP[1]) / TILESIZE

'''sensor set trans'''
sensor_trans = ((1, 0),
                (0, 1),
                (-1, 0),
                (0, -1))

'''environment data'''
FPS = 30

'''color'''
BLACK = (0, 0, 0)
WHITE = "#ffffff"
RED = "#ff0000"
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (140, 140, 140)
BLUE = (30, 60, 205)
LIGHT_BLUE = (33, 161, 241)
BROWN = (199, 178, 153)
PINK = (255, 105, 180)
MEDIUMPURPLE = (147, 112, 219)

'''object size'''
car_size = (60, 30)

'''data path'''
ASSET_IMAGE_DIR = path.join(path.dirname(__file__), "../asset/image")
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), '../asset/sound')

'''image'''
BG_IMG = "bg_img.png"
BG_URL = 'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/bg_img.png'

INFO_NAME = "info.png"
INFO_URL = 'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/info.png'

LOGO = "logo.png"
LOGO_URL = 'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/logo.png'

TMF_LOGO = "TMFlogo.png"
TMF_LOGO_URL = 'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/TMFlogo.png'

CARS_NAME = ["car_01.png", "car_02.png", "car_03.png", "car_04.png", "car_05.png", "car_06.png", ]
CARS_URL = ['https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/car_01.png',
            'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/car_02.png',
            'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/car_03.png',
            'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/car_04.png',
            'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/car_05.png',
            'https://raw.githubusercontent.com/yen900611/maze_car/master/asset/image/car_06.png'
            ]

'''map_file'''
PRACTICE_MAPS = ["level_1.json", "level_2.json", "level_3.json", "level_4.json", "level_5.json", "level_6.json"]
NORMAL_MAZE_MAPS = ["normal_map_1.json", "normal_map_2.json", "normal_map_3.json", "normal_map_3.json",
                    "normal_map_3.json", "normal_map_3.json"]
MOVE_MAZE_MAPS = ["move_map_1.json", "move_map_2.json", "move_map_3.json", "move_map_4.json", "move_map_4.json",
                  "move_map_4.json"]
