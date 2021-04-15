from os import path

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS

'''width and height'''
WIDTH =820
HEIGHT = 520
TILE_WIDTH = 480 #大小
TILE_HEIGHT = 480

'''tile-base'''
TILESIZE = 20
TILE_LEFTTOP = 20, 20 #pixel
GRIDWIDTH = (TILE_WIDTH + TILE_LEFTTOP[0])/TILESIZE
GRIDHEIGHT = (TILE_HEIGHT + TILE_LEFTTOP[1])/TILESIZE

'''environment data'''
FPS = 30

'''color'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
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

'''command'''
LEFT_cmd = "TURN_LEFT"
RIGHT_cmd = "TURN_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"

'''data path'''
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')

'''image'''
info_image = "info.png"
LOGO = "logo.png"

'''map_file'''
NORMAL_MAZE_MAPS = ["level_1.txt", "level_2.txt", "level_3.txt", "level_4.txt", "normal_map_1.txt", "normal_map_2.txt"]
MOVE_MAZE_MAPS = ["move_map_1.txt", "move_map_2.txt"]
MAZE_TEST = "map_test.txt"

