import time
import Box2D

from game_core.end_point import End_point
from game_core.maze_wall import Wall
from game_core.tilemap import Map, Camera
from game_core.maze_imformation import Normal_Maze_Size, Normal_Maze_Map
from .car import Car
from .gameMode import GameMode
from .env import *
import pygame


class MazeMode(GameMode):
    def __init__(self, user_num: int, maze_no, time, sound_controller):
        super(MazeMode, self).__init__()
        self.viewCenter = [WIDTH / 2 / PPM, HEIGHT / 2 / PPM]  # Box2D to Pygame
        self.game_end_time = time  # int, decide how many second the game will end even some users don't finish game
        self.ranked_user = []  # pygame.sprite car
        self.ranked_score = {"1P": 0, "2P": 0, "3P": 0, "4P": 0, "5P": 0, "6P": 0}  # 積分
        pygame.font.init()
        self.status = "GAME_PASS"
        self.is_end = False
        self.result = []
        self.x = 0
        self.maze_id = maze_no - 1
        self.map_file = NORMAL_MAZE_MAPS[self.maze_id]
        self.size = 1
        self.start_pos = (22, 3)
        self.wall_info = []
        '''set group'''
        self.car_info = []
        self.cars = pygame.sprite.Group()
        self.worlds = []
        self.all_sprites = pygame.sprite.Group()
        self._init_world(user_num)
        self._init_car()
        # self._init_maze(self.maze_id)
        self.eliminated_user = []
        self.user_time = []
        self.new()
        '''sound'''
        self.sound_controller = sound_controller

        '''image'''
        self.info = pygame.image.load(path.join(IMAGE_DIR, info_image))

    def update_sprite(self, command):
        '''update the model of game,call this fuction per frame'''
        self.car_info = []
        self.frame += 1
        self.handle_event()
        self._is_game_end()
        self.command = command
        for car in self.cars:
            car.update(command["ml_" + str(car.car_no + 1) + "P"])
            self.car_info.append(car.get_info())
            # self._is_car_arrive_end(car)
            car.detect_distance(self.frame, self.wall_info)
        self.all_sprites.update()
        for world in self.worlds:
            world.Step(TIME_STEP, 10, 10)
            world.ClearForces()
        if self.is_end:
            self.running = False
        # self.viewCenter[0] += 0.1

        # self.viewCenter = self.car.body.position[0], self.car.body.position[1]
        # self.camera.update(self.car)

    def new(self):
        self.load_data()
        self.walls = pygame.sprite.Group()
        self.get_wall_info()
        # print(self.wall_info)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    for world in self.worlds:
                        Wall(self, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)), world,
                                  len(self.map.data))
                elif tile == "E":
                    End_point(self, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)))
        self.camera = Camera(self.map.width, self.map.height)
        pass

    def get_wall_info(self):
        wall_tiles = []
        for row, tiles in enumerate(self.map.data):
            col = 0
            first_tile = -1
            last_tile = -1
            while col < (len(tiles)):
                if tiles[col] == "1":
                    if first_tile == -1:
                        first_tile = col
                        if col == len(tiles) -1:
                            last_tile = col
                            self.wall_vertices((first_tile, row), (last_tile, row))
                            # wall_tiles.append([(first_tile,row), (last_tile,row)])
                            first_tile = -1
                            col += 1
                        else:
                            col += 1
                    elif col == len(tiles) -1:
                        last_tile = col
                        self.wall_vertices((first_tile, row), (last_tile, row))
                        # wall_tiles.append([(first_tile,row), (last_tile,row)])
                        first_tile = -1
                        col += 1
                    else:
                        col += 1
                else:
                    if first_tile != -1:
                        last_tile = col - 1
                        self.wall_vertices((first_tile, row), (last_tile, row))
                        # wall_tiles.append([(first_tile,row), (last_tile,row)])
                        first_tile = -1
                        col += 1
                    else:
                        col += 1

    def wall_vertices(self, first_tile, last_tile):
        first_tilex = first_tile[0]+ TILESIZE/ (2*PPM) + 1
        first_tiley = GRIDHEIGHT + TILE_LEFTTOP[1] / PPM - first_tile[1] - TILESIZE/ (2*PPM) - 1
        last_tilex = last_tile[0]+ TILESIZE/ (2*PPM) + 1
        last_tiley = GRIDHEIGHT + TILE_LEFTTOP[1] / PPM - last_tile[1] - TILESIZE/ (2*PPM) - 1
        r = TILESIZE/ (2*PPM)
        vertices = [(first_tilex - r, first_tiley + r),
                    (last_tilex + r, last_tiley + r),
                    (last_tilex + r, last_tiley - r),
                    (first_tilex - r, first_tiley -r)
                    ] #Box2D
        self.wall_info.append([vertices[0],vertices[1]])
        self.wall_info.append([vertices[2],vertices[1]])
        self.wall_info.append([vertices[3],vertices[0]])
        self.wall_info.append([vertices[2],vertices[3]])
        return vertices
        pass

    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(path.dirname(__file__), "map")
        # img_folder = path.join(path.dirname(__file__), "image")
        self.map = Map(path.join(map_folder, self.map_file))
        pass

    def detect_collision(self):
        super(MazeMode, self).detect_collision()
        pass

    def _print_result(self):
        if self.is_end and self.x == 0:
            for user in self.ranked_user:
                self.result.append(str(user.car_no + 1) + "P:" + str(user.end_time) + "s")
                self.ranked_score[str(user.car_no + 1) + "P"] = user.score
            print("score:", self.ranked_score)
            self.x += 1
            print(self.result)
        pass

    def _init_world(self, user_no: int):
        for i in range(user_no):
            world = Box2D.b2.world(gravity=(0, 0), doSleep=True, CollideConnected=False)
            self.worlds.append(world)
        pass

    def _init_car(self):
        # if Normal_Maze_Size[self.maze_id] == 4:
        self.start_pos = (22, 3)
        # elif Normal_Maze_Size[self.maze_id] == 5:
        #     self.start_pos = (28, 3)
        # elif Normal_Maze_Size[self.maze_id] == 6:
        #     self.start_pos = (34, 3)
        for world in self.worlds:
            self.car = Car(world, self.start_pos, self.worlds.index(world), self.size)
            self.cars.add(self.car)
            self.car_info.append(self.car.get_info())
            pass

    def _init_maze(self, maze_no):
        for world in self.worlds:
            for wall in Normal_Maze_Map[maze_no]:
                wall_bottom = world.CreateKinematicBody(position=(0, 0), linearVelocity=(0, 0))
                box = wall_bottom.CreatePolygonFixture(vertices=wall)
        pass

    def _is_game_end(self):
        if self.frame > FPS * self.game_end_time or len(self.eliminated_user) == len(self.cars):
            print("game end")
            for car in self.cars:
                if car not in self.eliminated_user and car.status:
                    car.end_time = round(time.time() - self.start_time)
                    self.eliminated_user.append(car)
                    self.user_time.append(car.end_time)
                    car.status = False
            self.is_end = True
            self.rank()
            self._print_result()
            self.status = "GAME OVER"
        pass

    def _is_car_arrive_end(self, car):
        if car.status:
            if car.body.position[1] > 6 * Normal_Maze_Size[self.maze_id] + 1:
                car.end_time = round(time.time() - self.start_time)
                self.eliminated_user.append(car)
                self.user_time.append(car.end_time)
                car.status = False
        pass

    def draw_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(MazeMode, self).draw_bg()
        self.screen.fill(BLACK)
        self.screen.blit(self.info, pygame.Rect(507, 20, 306, 480))
        if self.is_end == False:
            self.draw_time(time.time())
        '''畫出每台車子的資訊'''
        self._draw_user_imformation()

    def drawWorld(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(MazeMode, self).drawWorld()
        # self.all_sprites.draw(self.screen)
        # self.draw_grid()
        # for sprite in self.all_sprites:
        #     pygame.draw.rect(self.screen, RED, sprite.rect, 2)
        # for wall in self.wall_info:
            # pygame.draw.circle(self.screen, WHITE, (0*PPM, HEIGHT - 0*PPM), 5)
            # pygame.draw.circle(self.screen, WHITE, (1*PPM, HEIGHT - 1*PPM), 5)
            # pygame.draw.line(self.screen, GREY, (wall[0][0]*PPM, HEIGHT - wall[0][1]*PPM), (wall[1][0]*PPM, HEIGHT - wall[1][1]*PPM), 3)
        for wall in self.walls:
            vertices = [(wall.body.transform * v) for v in wall.box.shape.vertices]
            vertices = [(v[0] - self.viewCenter[0] + WIDTH / (PPM * 2), self.viewCenter[1] - v[1] + HEIGHT / (PPM * 2))
                        for v in vertices]
            vertices = [(v[0] * PPM, v[1] * PPM) for v in vertices]
            pygame.draw.polygon(self.screen, WHITE, vertices)
        # for car in self.cars:
            # pygame.draw.rect(self.screen, GREEN, car.rect, 2)
            # pygame.draw.circle(self.screen, GREEN, (car.sensor.sensor_right.position[0]*PPM,HEIGHT - car.sensor.sensor_right.position[1]*PPM),
            #                    5)
            #
            # pygame.draw.circle(self.screen, GREEN, (car.sensor.sensor_left.position[0]*PPM,HEIGHT - car.sensor.sensor_left.position[1]*PPM),
            #                    5)
            # pygame.draw.polygon(self.screen, BLUE, car.vertices)

            # vertices = [(car.body.transform * v) for v in car.box.shape.vertices]
            # vertices = [(v[0] - self.viewCenter[0] + WIDTH/(PPM * 2), self.viewCenter[1] - v[1] + HEIGHT/(PPM * 2)) for v in vertices]
            # vertices = [(v[0] * PPM, v[1] * PPM) for v in vertices]
            # pygame.draw.polygon(self.screen, WHITE, vertices)

        self.cars.draw(self.screen)

    def _draw_user_imformation(self):
        for i in range(6):
            for car in self.cars:
                if car.car_no == i:
                    if i % 2 == 0:
                        if car.status:
                            self.draw_information(self.screen, YELLOW, "L:" + str(car.sensor_L) + "cm", 600,
                                                  178 + 20 + 94 * i / 2)
                            self.draw_information(self.screen, RED, "F:" + str(car.sensor_F) + "cm", 600,
                                                  178 + 40 + 94 * i / 2)
                            self.draw_information(self.screen, LIGHT_BLUE, "R:" + str(car.sensor_R) + "cm", 600,
                                                  178 + 60 + 94 * i / 2)
                        else:
                            self.draw_information(self.screen, WHITE, str(car.end_time) + "s",
                                                  600, 178 + 40 + 94 * (i // 2))

                    else:
                        if car.status:
                            self.draw_information(self.screen, YELLOW, "L:" + str(car.sensor_L) + "cm", 730,
                                                  178 + 20 + 94 * (i // 2))
                            self.draw_information(self.screen, RED, "F:" + str(car.sensor_F) + "cm", 730,
                                                  178 + 40 + 94 * (i // 2))
                            self.draw_information(self.screen, LIGHT_BLUE, "R:" + str(car.sensor_R) + "cm", 730,
                                                  178 + 60 + 94 * (i // 2))
                        else:
                            self.draw_information(self.screen, WHITE, str(car.end_time) + "s",
                                                  730, 178 + 40 + 94 * (i // 2))

    def rank(self):
        while len(self.eliminated_user) > 0:
            for car in self.eliminated_user:
                if car.end_time == min(self.user_time):
                    self.ranked_user.append(car)
                    self.user_time.remove(car.end_time)
                    self.eliminated_user.remove(car)
        for i in range(len(self.ranked_user)):
            if self.ranked_user[i].end_time == self.ranked_user[i - 1].end_time:
                if i == 0:
                    self.ranked_user[i].score = 6
                else:
                    for j in range(1, i + 1):
                        if self.ranked_user[i - j].end_time == self.ranked_user[i].end_time:
                            if i == j:
                                self.ranked_user[i].score = 6
                            else:
                                pass
                            pass
                        else:
                            self.ranked_user[i].score = 6 - (i - j + 1)
                            break
            else:
                self.ranked_user[i].score = 6 - i

    def draw_grid(self):
        for x in range(TILE_LEFTTOP[0], TILE_WIDTH + TILE_LEFTTOP[0], TILESIZE):
            pygame.draw.line(self.screen, GREY, (x, TILE_LEFTTOP[1]), (x, TILE_HEIGHT + TILE_LEFTTOP[1]))
        for y in range(TILE_LEFTTOP[1], TILE_HEIGHT + TILE_LEFTTOP[1], TILESIZE):
            pygame.draw.line(self.screen, GREY, (TILE_LEFTTOP[0], y), (TILE_WIDTH + TILE_LEFTTOP[0], y))
