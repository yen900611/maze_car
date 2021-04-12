import math
import time
import Box2D

from .points import End_point
from .maze_imformation import Move_Maze_Size, Move_Maze, Normal_Maze_Size
from .maze_wall import Move_Wall
from .car import Car
from .gameMode import GameMode
from .env import *
import pygame
# from .maze_wall import Wall


class MoveMazeMode(GameMode):
    def __init__(self, user_num: int, maze_no, time, sound_controller):
        super(MoveMazeMode, self).__init__()
        self.user_check_points = []
        self.game_end_time = time  # int, decide how many second the game will end even some users don't finish game
        self.ranked_user = []  # pygame.sprite car
        self.ranked_score = {"1P": 0, "2P": 0, "3P": 0, "4P": 0, "5P": 0, "6P": 0}  # 積分
        pygame.font.init()
        self.status = "GAME_PASS"
        self.is_end = False
        self.result = []
        self.x = 0
        self.maze_id = maze_no - 1
        self.size = 4 / Move_Maze_Size[self.maze_id]
        self.start_pos = (22, 3)

        '''set group'''
        self.car_info = []
        self.cars = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.all_points = pygame.sprite.Group()
        self.worlds = []
        self._init_world(user_num)
        self._init_car()
        self._init_maze(self.maze_id)
        self.eliminated_user = []
        self.user_time = []
        self.wall_information = []

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
        self.walls.update()
        self.wall_information = []
        for wall in self.walls:
            for info in wall.wall_info:
                self.wall_information.append(info)
        for car in self.cars:
            car.update(command["ml_" + str(car.car_no + 1) + "P"])
            self.get_polygon_vertice(car)
            self.car_info.append(car.get_info())
            self._is_car_arrive_end(car)
            car.detect_distance(self.frame, self.wall_information)
        self.all_points.update()
        for world in self.worlds:
            world.Step(TIME_STEP, 10, 10)
            world.ClearForces()
        if self.is_end:
            self.running = False

    def detect_collision(self):
        super(MoveMazeMode, self).detect_collision()
        pass

    def _print_result(self):
        if self.is_end and self.x == 0:
            for rank in self.ranked_user:
                for user in rank:
                    self.result.append(str(user.car_no + 1) + "P:" + str(user.end_frame) + "frame")
            self.x += 1
            print(self.result)
        pass

    def _init_world(self, user_no: int):
        for i in range(user_no):
            world = Box2D.b2.world(gravity=(0, 0), doSleep=True, CollideConnected=False)
            self.worlds.append(world)
        pass

    def _init_car(self):
        if Move_Maze_Size[self.maze_id] == 3:
            self.start_pos = (16, 3)
            self.end_point = End_point(self, (0,0))
            self.end_point.rect.center = (100, 30)
        elif Move_Maze_Size[self.maze_id] == 4:
            self.start_pos = (22, 3)
            self.end_point = End_point(self, (0,0))
            self.end_point.rect.center = (60, 30)
        elif Move_Maze_Size[self.maze_id] == 5:
            self.start_pos = (28, 3)
        elif Move_Maze_Size[self.maze_id] == 6:
            self.start_pos = (34, 3)
        for world in self.worlds:
            self.car = Car(world, self.start_pos, self.worlds.index(world), self.size)
            self.cars.add(self.car)
            self.car_info.append(self.car.get_info())
            pass

    def _init_maze(self, maze_no):
        for world in self.worlds:
            for wall in Move_Maze[maze_no]:
                maze_wall = Move_Wall(world, wall["vertices_init"], self.size, wall["is_move"], velocity=wall["velocity"],
                                 vertices_end=wall["vertices_end"])
                self.walls.add(maze_wall)
        pass

    def _is_game_end(self):
        if self.frame > FPS * self.game_end_time or len(self.eliminated_user) == len(self.cars):
            for car in self.cars:
                if car not in self.eliminated_user and car.status:
                    car.end_frame = self.frame
                    self.eliminated_user.append(car)
                    self.user_check_points.append(car.check_point)
                    self.user_time.append(car.end_frame)
                    car.status = False
            self.is_end = True
            self.ranked_user = self.rank()
            self._print_result()
            self.status = "GAME OVER"
        pass

    def _is_car_arrive_end(self, car):
        if car.status:
            if car.body.position[1] > 6 * Move_Maze_Size[self.maze_id] + 1:

                car.end_frame = round(time.time() - self.start_time)
                self.eliminated_user.append(car)
                self.user_time.append(car.end_frame)
                car.status = False

    def get_polygon_vertice(self, car):
        car.vertices = [(car.body.transform * v) * PPM * car.maze_size for v in car.box.shape.vertices]
        car.vertices = [(v[0], HEIGHT - v[1]) for v in car.vertices]
        car.image = pygame.transform.rotate(car.origin_image, (car.body.angle * 180 / math.pi) % 360)
        car.rect = car.image.get_rect()
        car.rect.center = car.body.position[0] * PPM * car.maze_size, HEIGHT - car.body.position[
            1] * PPM * car.maze_size

    def draw_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(MoveMazeMode, self).draw_bg()
        self.screen.fill(BLACK)
        self.screen.blit(self.info, pygame.Rect(507, 20, 306, 480))
        if self.is_end == False:
            self.draw_time(self.frame)
        pass

        '''畫出每台車子的資訊'''
        self._draw_user_imformation()

    def drawWorld(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(MoveMazeMode, self).drawWorld()
        for wall in self.walls:
            vertices = [(wall.body.transform * v) * PPM * self.size for v in wall.box.shape.vertices]
            vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(self.screen, WHITE, vertices)

        self.cars.draw(self.screen)
        self.all_points.draw(self.screen)
        pass

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
                            self.draw_information(self.screen, WHITE, str(car.end_frame) + "s",
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
                            self.draw_information(self.screen, WHITE, str(car.end_frame) + "s",
                                                  730, 178 + 40 + 94 * (i // 2))

    def rank(self):
        while len(self.eliminated_user) > 0:
            for car in self.eliminated_user:
                if car.is_completed:
                    self.ranked_user.append(car)
                    self.eliminated_user.remove(car)
                else:
                    if car.check_point == max(self.user_check_points):
                        self.ranked_user.append(car)
                        self.user_check_points.remove(car.check_point)
                        self.eliminated_user.remove(car)
        same_rank = []
        rank_user = [] # [[sprite, sprite],[]]
        for user in self.ranked_user:
            if not same_rank:
                same_rank.append(user)
            else:
                if user.is_completed:
                    if user.end_frame == same_rank[0].end_frame:
                        same_rank.append(user)
                    else:
                        rank_user.append(same_rank)
                        same_rank = []
                        same_rank.append(user)
                else:
                    if same_rank[0].is_completed:
                        rank_user.append(same_rank)
                        same_rank = []
                        same_rank.append(user)
                    else:
                        if user.check_point == same_rank[0].check_point:
                            same_rank.append(user)
                        else:
                            rank_user.append(same_rank)
                            same_rank = []
                            same_rank.append(user)
        if same_rank:
            rank_user.append(same_rank)
        return rank_user
