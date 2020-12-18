from os import path

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS

'''width and height'''
WIDTH = 820
HEIGHT = 520

'''environment data'''
FPS = 30

'''color'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (140,140,140)
BLUE = (30,60,205)
LIGHT_BLUE = (33, 161, 241)
BROWN = (199, 178, 153)
MEDIUMPURPLE = (147, 112, 219)
car_color1 = [WHITE, LIGHT_BLUE, MEDIUMPURPLE]
car_color2 = [YELLOW, RED, GREEN]


'''Maze'''
Maze = [
    [[(1,1), (25,1), (1,1.5), (25,1.5)], [(25,1), (25,25), (24.5,1), (24.5,25)], [(1,1), (1,25), (1.5,1), (1.5,25)],
     [(7, 25), (25, 25), (7, 24.5), (25, 24.5)], [(18.5,1), (18.5,19), (19,1), (19,19)], [(1,7), (7,7), (1,7.5), (7,7.5)],
     [(7, 19), (13, 19), (7, 19.5), (13, 19.5)], [(13,7), (13,25), (12.5,7), (12.5,25)], [(7,7), (7,13), (7.5, 7), (7.5,13)]
     ],
]
wall_info =[
    [(1,1), (25,1)], [(25,1), (25,25)], [(1,1), (1,25)], [(7, 25), (25, 25)], [(18.5,1), (18.5,19)], [(19,1), (19,19)],[(1,7), (7,7)],
    [(1,7.5), (7,7.5)], [(7, 19), (13, 19)], [(7, 19.5), (13, 19.5)], [(13,7), (13,25)], [(12.5,7), (12.5,25)], [(7,7), (7,13)], [(7.5, 7), (7.5,13)]
]

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
