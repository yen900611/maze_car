import time
import Box2D
from .sound_controller import SoundController
from .points import End_point, Check_point, Outside_point
from .maze_wall import Wall
from .tilemap import Map, Camera
from .maze_imformation import Normal_Maze_Size, Normal_Maze_Map
from .car import Car
from .gameMode import GameMode
from .env import *
import pygame

class MazeMode(GameMode):
    def __init__(self, user_num: int, maze_no, time, sound_controller):
        super(MazeMode, self).__init__()
        '''load map data'''
        self.user_num = user_num
        self.maze_id = maze_no - 1
        self.map_file = NORMAL_MAZE_MAPS[self.maze_id]
        self.load_data()

        '''group of sprites'''
        self.worlds = []
        self.cars = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.all_points = pygame.sprite.Group() # Group inclouding end point, check points,etc.

        '''data set'''
        self.wall_info = []
        self.wall_vertices_for_Box2D = []
        self.car_info = []
        self.ranked_user = []  # pygame.sprite car
        self.result = []
        self.eliminated_user = []

        self.game_end_time = time  # int, decide how many second the game will end even some users don't finish game
        pygame.font.init()
        self.status = "GAME_PASS"
        self.is_end = False
        self.x = 0
        self._init_world(user_num)
        self.new()
        '''sound'''
        self.sound_controller = SoundController(sound_controller)

    def new(self):
        # initialize all variables and do all setup for a new game

        self.get_wall_info_h("1")
        self.get_wall_info_v("1")
        for wall_vertices in self.wall_vertices_for_Box2D:
            for world in self.worlds:
                wall = Wall(self, wall_vertices["vertices"], world)
                if self.worlds.index(world) == 0:
                    self.walls.add(wall)
        for wall in self.walls:
            vertices = [(wall.body.transform * v) for v in wall.box.shape.vertices]
            self.wall_info.append([vertices[0], vertices[1]])
            self.wall_info.append([vertices[2], vertices[1]])
            self.wall_info.append([vertices[3], vertices[0]])
            self.wall_info.append([vertices[2], vertices[3]])
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    for world in self.worlds:
                        x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                        self.car = Car(world, (x + TILESIZE / (2 * PPM), - y - TILESIZE / (2 * PPM)),
                                       self.worlds.index(world))
                        self.cars.add(self.car)
                        self.car_info.append(self.car.get_info())
                        # Car(self, world, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)), i, 1)
                elif tile == "E":
                    self.end_point = End_point(self,
                                               (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)))
                elif tile == "C":
                    Check_point(self, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)))

                elif tile == "O":
                    Outside_point(self, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)))
        self.pygame_point = [self.car.body.position[0] - (TILE_LEFTTOP[0] + TILE_WIDTH) / 2 / PPM,
                             self.car.body.position[1] + HEIGHT / 2 / PPM]
        self.limit_pygame_screen()

    def update_sprite(self, command):
        '''update the model of game,call this fuction per frame'''
        self.car_info.clear()
        self.frame += 1
        self.handle_event()
        self._is_game_end()
        self.command = command
        self.limit_pygame_screen()
        for car in self.cars:
            car.update(command["ml_" + str(car.car_no + 1) + "P"])
            car.rect.center = self.trnsfer_box2d_to_pygame(car.body.position)
            self.car_info.append(car.get_info())
            car.detect_distance(self.frame, self.wall_info)

        self.all_points.update()
        for point in self.all_points:
            point.rect.x, point.rect.y = self.trnsfer_box2d_to_pygame((point.x + TILESIZE/2/PPM, -point.y - TILESIZE/2/PPM))
        for world in self.worlds:
            world.Step(TIME_STEP, 10, 10)
            world.ClearForces()
        if self.is_end:
            self.running = False

    def limit_pygame_screen(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.pygame_point[1] += 0.2
        elif keystate[pygame.K_s]:
            self.pygame_point[1] -= 0.2
        elif keystate[pygame.K_a]:
            self.pygame_point[0] -= 0.2
        elif keystate[pygame.K_d]:
            self.pygame_point[0] += 0.2

        if self.pygame_point[1] > 0:
            self.pygame_point[1] = 0
        elif self.pygame_point[1] < TILE_HEIGHT/PPM-self.map.tileHeight:
            self.pygame_point[1] = TILE_HEIGHT/PPM-self.map.tileHeight
        else:
            pass
        if self.pygame_point[0] >self.map.tileWidth-TILE_WIDTH/PPM:
            self.pygame_point[0] = self.map.tileWidth-TILE_WIDTH/PPM
        elif self.pygame_point[0] < 0:
            self.pygame_point[0] = 0
        else:
            pass

    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(path.dirname(__file__), "map")
        self.map = Map(path.join(map_folder, self.map_file))

    def _init_world(self, user_no: int):
        for i in range(user_no):
            world = Box2D.b2.world(gravity=(0, 0), doSleep=True, CollideConnected=False)
            self.worlds.append(world)

    def _is_game_end(self):
        if self.frame > FPS * self.game_end_time or len(self.eliminated_user) == len(self.cars):
            print("game end")
            for car in self.cars:
                if car not in self.eliminated_user and car.status:
                    car.end_frame = self.frame
                    self.eliminated_user.append(car)
                    car.status = False
            self.is_end = True
            self.ranked_user = self.rank()
            self._print_result()
            self.status = "GAME OVER"

    def draw_grid(self):
        for x in range(TILE_LEFTTOP[0], TILE_WIDTH + TILE_LEFTTOP[0], TILESIZE):
            pygame.draw.line(self.screen, GREY, (x, TILE_LEFTTOP[1]), (x, TILE_HEIGHT + TILE_LEFTTOP[1]))
        for y in range(TILE_LEFTTOP[1], TILE_HEIGHT + TILE_LEFTTOP[1], TILESIZE):
            pygame.draw.line(self.screen, GREY, (TILE_LEFTTOP[0], y), (TILE_WIDTH + TILE_LEFTTOP[0], y))