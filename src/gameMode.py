"""
This is a base class for different mode in game.
"""
from .car import Car
from .points import *
from .maze_wall import SlantWall

import pygame

from .env import *


class GameMode(object):
    def __init__(self, bg_img=pygame.Surface((WIDTH, HEIGHT))):
        self.bg_img = bg_img
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame = 0
        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.match_font("arial", bold=True), 15)
        self.time_font = pygame.font.Font(pygame.font.match_font("arial", bold=True), 46)
        self.check_point_num = 0
        # self.start_time = time.time()

    def ticks(self, fps=FPS):
        """This method should be called once per frame.
        It will compute how many milliseconds have passed since the previous call.
        :param fps: frame per second 每秒的繪圖次數
        :return: None
        """
        self.clock.tick(fps)

    def handle_event(self):
        """ Handle the event from window , mouse or button.
        :return: None
        """
        pass

    def detect_collision(self):
        """ Detect the collision event between sprites.
        :return: None
        """
        pass

    def update_sprite(self, *args):
        """ This function should update every sprite in games.
        :return: None
        """
        pass

    def draw_bg(self):
        """  Draw a background on screen.
        :return:None
        """
        pass

    def drawWorld(self):
        """  This function should draw every sprite on specific surface.
        :return: None
        """
        pass

    def flip(self):
        """Update the full display Surface to the screen
        :return:None
        """
        pygame.display.flip()

    def isRunning(self) -> bool:
        return self.running

    def rank(self):
        completed_game_user = []
        unfinish_game_user = []
        user_end_frame = []
        user_check_point = []
        for car in self.eliminated_user:
            if car.is_completed:
                user_end_frame.append(car.end_frame)
                completed_game_user.append(car)
            else:
                user_check_point.append(car.check_point)
                unfinish_game_user.append(car)
        same_rank = []
        rank_user = []  # [[sprite, sprite],[]]

        result = [user_end_frame.index(x) for x in sorted(user_end_frame)]
        for i in range(len(result)):
            if result[i] != result[i - 1] or i == 0:
                if same_rank:
                    rank_user.append(same_rank)
                same_rank = []
                same_rank.append(completed_game_user[result[i]])
            else:
                for user in completed_game_user:
                    if user.end_frame == same_rank[0].end_frame and user not in same_rank:
                        same_rank.append(user)
                    else:
                        pass
        if same_rank:
            rank_user.append(same_rank)

        same_rank = []
        result = [user_check_point.index(x) for x in sorted(user_check_point, reverse=True)]
        for i in range(len(result)):
            if result[i] != result[i - 1] or i == 0:
                if same_rank:
                    rank_user.append(same_rank)
                same_rank = []
                same_rank.append(unfinish_game_user[result[i]])
            else:
                for user in unfinish_game_user:
                    if user.check_point == same_rank[0].check_point and user not in same_rank:
                        same_rank.append(user)
                    else:
                        pass
        if same_rank:
            rank_user.append(same_rank)
        return rank_user

    def trnsfer_box2d_to_pygame(self, coordinate):
        '''
        :param coordinate: vertice of body of box2d object
        :return: center of pygame rect
        '''
        return ((coordinate[0] - self.pygame_point[0]) * PPM, (self.pygame_point[1] - coordinate[1]) * PPM)

    def get_wall_info_v(self, wall_tile):
        wall_tiles = []
        for col in range(len(self.map.data[0]) - 1):
            row = 0
            first_tile = -1
            last_tile = -1
            while row < len(self.map.data):
                tiles = self.map.data[row]

                if (tiles[col]%18) == wall_tile:
                    if first_tile == -1:
                        first_tile = row
                        if row == len(self.map.data) - 1:
                            last_tile = row
                            self.wall_vertices_for_Box2D.append(
                                {"type": wall_tile,
                                 "vertices": self.wall_vertices_v((col, first_tile), (col, last_tile))})

                            # self.wall_vertices_for_Box2D.append(self.wall_vertices_v((col, first_tile), (col, last_tile)))
                            first_tile = -1
                            row += 1
                        else:
                            row += 1
                    elif row == len(self.map.data) - 1:
                        last_tile = row
                        self.wall_vertices_for_Box2D.append(
                            {"type": wall_tile, "vertices": self.wall_vertices_v((col, first_tile), (col, last_tile))})
                        # self.wall_vertices_for_Box2D.append(self.wall_vertices_v((col, first_tile), (col, last_tile)))
                        first_tile = -1
                        row += 1
                    else:
                        row += 1
                else:
                    if first_tile != -1:
                        last_tile = row - 1
                        self.wall_vertices_for_Box2D.append(
                            {"type": wall_tile, "vertices": self.wall_vertices_v((col, first_tile), (col, last_tile))})
                        # self.wall_vertices_for_Box2D.append(self.wall_vertices_v((col, first_tile), (col, last_tile)))
                        first_tile = -1
                        row += 1
                    else:
                        row += 1

    def get_wall_info_h(self, wall_tile):
        wall_tiles = []
        for row, tiles in enumerate(self.map.data):
            col = 0
            first_tile = -1
            last_tile = -1
            while col < (len(tiles)):
                if (tiles[col]%18) == wall_tile:
                    if first_tile == -1:
                        first_tile = col
                        if col == len(tiles) - 1:
                            first_tile = -1
                            col += 1
                        else:
                            col += 1
                    elif col == len(tiles) - 1:
                        last_tile = col
                        self.wall_vertices_for_Box2D.append(
                            {"type": wall_tile, "vertices": self.wall_vertices_h((first_tile, row), (last_tile, row))})
                        # self.wall_vertices_for_Box2D.append(self.wall_vertices_h((first_tile, row), (last_tile, row)))
                        for i in range(first_tile, last_tile + 1):
                            tiles[i] = 0
                        first_tile = -1
                        col += 1
                    else:
                        col += 1
                else:
                    if first_tile != -1:
                        last_tile = col - 1
                        if first_tile == last_tile:
                            first_tile = -1
                            col += 1
                        else:
                            self.wall_vertices_for_Box2D.append(
                                {"type": wall_tile,
                                 "vertices": self.wall_vertices_h((first_tile, row), (last_tile, row))})
                            for i in range(first_tile, last_tile + 1):
                                tiles[i] = 0
                            first_tile = -1
                            col += 1
                    else:
                        col += 1

    def wall_vertices_h(self, first_tile, last_tile):
        first_tilex = first_tile[0] + TILESIZE / (2 * PPM) + 1
        first_tiley = - first_tile[1] - TILESIZE / (2 * PPM) - 1
        last_tilex = last_tile[0] + TILESIZE / (2 * PPM) + 1
        last_tiley = - last_tile[1] - TILESIZE / (2 * PPM) - 1
        r = TILESIZE / (2 * PPM)
        vertices = [(first_tilex - r, first_tiley + r),
                    (last_tilex + r, last_tiley - r),
                    (last_tilex + r, last_tiley + r),
                    (first_tilex - r, first_tiley - r),

                    ]  # Box2D

        # self.wall_info.append([vertices[0],vertices[1]])
        # self.wall_info.append([vertices[2],vertices[1]])
        # self.wall_info.append([vertices[3],vertices[0]])
        # self.wall_info.append([vertices[2],vertices[3]])
        return vertices

    def wall_vertices_v(self, first_tile, last_tile):
        first_tilex = first_tile[0] + TILESIZE / (2 * PPM) + 1
        first_tiley = - first_tile[1] - TILESIZE / (2 * PPM) - 1
        last_tilex = last_tile[0] + TILESIZE / (2 * PPM) + 1
        last_tiley = - last_tile[1] - TILESIZE / (2 * PPM) - 1
        r = TILESIZE / (2 * PPM)
        vertices = [(first_tilex - r, first_tiley + r),
                    (first_tilex + r, first_tiley + r),
                    (last_tilex + r, last_tiley - r),
                    (last_tilex - r, last_tiley - r),

                    ]  # Box2D

        # self.wall_info.append([vertices[0],vertices[1]])
        # self.wall_info.append([vertices[2],vertices[1]])
        # self.wall_info.append([vertices[3],vertices[0]])
        # self.wall_info.append([vertices[2],vertices[3]])
        return vertices

    def _print_result(self):
        if self.is_end and self.x == 0:
            for rank in self.ranked_user:
                for user in rank:
                    self.result.append(str(user.car_no + 1) + "P:" + str(user.end_frame) + "frame")
            self.x += 1
            print(self.result)

    def load_map_object(self):
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                try:
                    if tile == 6 or tile == 10:
                        for world in self.worlds:
                            x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                            self.car = Car(world, (x + TILESIZE / (2 * PPM), - y - TILESIZE / (2 * PPM)),
                                           self.worlds.index(world), self.sensor_num, 2)
                            self.cars.add(self.car)
                            self.car_info.append(self.car.get_info())
                            # Car(self, world, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)), i, 1)
                    elif tile == 7:
                        self.end_point = End_point(self,
                                                   (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)))
                    elif tile == 8:
                        Check_point(self, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)))
                        self.check_point_num+=1
                    elif tile == 9:
                        Outside_point(self, (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE)))
                    elif tile == 13:
                        for world in self.worlds:
                            x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                            self.car = Car(world, (x + TILESIZE / (2 * PPM), - y - TILESIZE / (2 * PPM)),
                                           self.worlds.index(world), self.sensor_num, 0.5)
                            self.cars.add(self.car)
                            self.car_info.append(self.car.get_info())
                    elif tile == 12:
                        for world in self.worlds:
                            x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                            self.car = Car(world, (x + TILESIZE / (2 * PPM), - y - TILESIZE / (2 * PPM)),
                                           self.worlds.index(world), self.sensor_num, 1)
                            self.cars.add(self.car)
                            self.car_info.append(self.car.get_info())
                    elif tile == 11:
                        for world in self.worlds:
                            x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                            self.car = Car(world, (x + TILESIZE / (2 * PPM), - y - TILESIZE / (2 * PPM)),
                                           self.worlds.index(world), self.sensor_num, 1.5)
                            self.cars.add(self.car)
                            self.car_info.append(self.car.get_info())
                    elif tile == 14:
                        x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                        wall_vertices = [(x, -y),
                                         (x + (TILE_LEFTTOP[0] / TILESIZE), -y),
                                         (x + (TILE_LEFTTOP[0] / TILESIZE), -y - (TILE_LEFTTOP[0] / TILESIZE))]
                        for world in self.worlds:
                            wall = SlantWall(self, wall_vertices, world)
                            if self.worlds.index(world) == 0:
                                self.slant_walls.add(wall)
                    elif tile == 15:
                        x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                        wall_vertices = [(x, -y - (TILE_LEFTTOP[0] / TILESIZE)),
                                         (x + (TILE_LEFTTOP[0] / TILESIZE), -y),
                                         (x + (TILE_LEFTTOP[0] / TILESIZE), -y - (TILE_LEFTTOP[0] / TILESIZE))]
                        for world in self.worlds:
                            wall = SlantWall(self, wall_vertices, world)
                            if self.worlds.index(world) == 0:
                                self.slant_walls.add(wall)
                    elif tile == 16:
                        x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                        wall_vertices = [(x, -y - (TILE_LEFTTOP[0] / TILESIZE)),
                                         (x, -y),
                                         (x + (TILE_LEFTTOP[0] / TILESIZE), -y - (TILE_LEFTTOP[0] / TILESIZE))]
                        for world in self.worlds:
                            wall = SlantWall(self, wall_vertices, world)
                            if self.worlds.index(world) == 0:
                                self.slant_walls.add(wall)
                    elif tile == 17:
                        x, y = (col + (TILE_LEFTTOP[0] / TILESIZE), row + (TILE_LEFTTOP[1] / TILESIZE))
                        wall_vertices = [(x, -y - (TILE_LEFTTOP[0] / TILESIZE)),
                                         (x, -y),
                                         (x + (TILE_LEFTTOP[0] / TILESIZE), -y)]
                        for world in self.worlds:
                            wall = SlantWall(self, wall_vertices, world)
                            if self.worlds.index(world) == 0:
                                self.slant_walls.add(wall)
                except Exception:
                    print("Map Error")
        try:
            if self.end_point and len(self.cars):
                pass
            else:
                print("Map without car")
                self.running = False
        except:
            print("Map without end point")
            self.running = False

