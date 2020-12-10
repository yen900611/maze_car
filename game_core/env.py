from os import path

'''width and height'''
WIDTH = 720
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
BLUE = (3,28,252)
LIGHT_BLUE = (33, 161, 241)

'''Maze'''
Maze1 = []
Maze2 = []
Maze3 = []

'''object size'''
car_size = (60, 30)

'''command'''
LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"

'''data path'''
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')
