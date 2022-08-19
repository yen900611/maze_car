from mlgame.utils.enum import get_ai_name
from .gameMode import GameMode
from .maze_wall import *
from .sound_controller import SoundController
from mlgame.game.paia_game import GameResultState
from .tilemap import Map


class MoveMazeMode(GameMode):
    def __init__(self, user_num: int, maze_no, time, sensor, sound_controller):
        super(MoveMazeMode, self).__init__()
        '''load map data'''
        self.user_num = user_num
        self.maze_id = maze_no - 1
        self.map_file = "move_map_" + str(maze_no) + ".json"
        self.load_data()

        '''group of sprites'''
        self.worlds = []
        self.cars = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.slant_walls = pygame.sprite.Group()
        self.wall_for_update = pygame.sprite.Group()
        self.all_points = pygame.sprite.Group()  # Group inclouding end point, check points,etc.

        '''data set'''

        self.wall_info = []
        self.wall_vertices_for_Box2D = []
        self.car_info = []
        self.ranked_user = []  # pygame.sprite car
        self.result = []
        self.eliminated_user = []
        self.user_check_points = []

        self.game_end_time = time  # int, decide how many frames the game will end even some users don't finish game
        pygame.font.init()
        self.state = GameResultState.FAIL
        self.is_end = False
        self.sensor_num = sensor
        self.x = 0
        self._init_world(user_num)
        self.new()
        '''sound'''
        self.sound_controller = SoundController(sound_controller)

    def new(self):
        # initialize all variables and do all setup for a new game
        self.get_wall_info_v(2)
        self.get_wall_info_h(3)
        self.get_wall_info_h(1)
        self.get_wall_info_v(1)
        self.get_wall_info_v(4)
        self.get_wall_info_h(5)
        self.load_map_object()
        for wall_vertices in self.wall_vertices_for_Box2D:
            if wall_vertices["type"] == 1:
                for world in self.worlds:
                    wall = Wall(self, wall_vertices["vertices"], world)
                    if self.worlds.index(world) == 0:
                        self.walls.add(wall)
            elif wall_vertices["type"] == 2:
                for world in self.worlds:
                    wall = VerticalMoveWall(self, wall_vertices["vertices"], world, 4, 5)
                    self.wall_for_update.add(wall)
                    if self.worlds.index(world) == 0:
                        self.walls.add(wall)
            elif wall_vertices["type"] == 3:
                for world in self.worlds:
                    wall = HorizontalMoveWall(self, wall_vertices["vertices"], world, 3, 6)
                    self.wall_for_update.add(wall)
                    if self.worlds.index(world) == 0:
                        self.walls.add(wall)
            elif wall_vertices["type"] == 4:
                for world in self.worlds:
                    wall = VerticalMoveWall(self, wall_vertices["vertices"], world, 3, -5)
                    self.wall_for_update.add(wall)
                    if self.worlds.index(world) == 0:
                        self.walls.add(wall)
            elif wall_vertices["type"] == 5:
                for world in self.worlds:
                    wall = HorizontalMoveWall(self, wall_vertices["vertices"], world, 5, -7)
                    self.wall_for_update.add(wall)
                    if self.worlds.index(world) == 0:
                        self.walls.add(wall)

        self.pygame_point = [0, 0]

    def update_sprite(self, command):
        '''update the model of game,call this fuction per frame'''
        self.car_info.clear()
        self.frame += 1
        self.handle_event()
        self._is_game_end()
        self.command = command
        self.wall_for_update.update()
        self.wall_info.clear()
        for wall in self.walls:
            vertices = [(wall.body.transform * v) for v in wall.box.shape.vertices]
            self.wall_info.append([vertices[0], vertices[1]])
            self.wall_info.append([vertices[2], vertices[1]])
            self.wall_info.append([vertices[3], vertices[0]])
            self.wall_info.append([vertices[2], vertices[3]])
        for wall in self.slant_walls:
            vertices = [(wall.body.transform * v) for v in wall.box.shape.vertices]
            self.wall_info.append([vertices[0], vertices[1]])
            self.wall_info.append([vertices[1], vertices[2]])
            self.wall_info.append([vertices[2], vertices[0]])
        for car in self.cars:
            car.update(command[get_ai_name(car.car_no)])
            car.rect.center = self.trnsfer_box2d_to_pygame(car.body.position)
            self.car_info.append(car.get_info())
            car.detect_distance(self.frame, self.wall_info)

        for point in self.all_points:
            point.rect.x, point.rect.y = self.trnsfer_box2d_to_pygame((point.x, point.y))
        self.all_points.update()
        for world in self.worlds:
            world.Step(TIME_STEP, 10, 10)
            world.ClearForces()
        if self.is_end:
            self.running = False

    def load_data(self):
        map_folder = path.join(path.dirname(__file__), "map")
        try:
            self.map = Map(path.join(map_folder, self.map_file))
        except Exception:
            print(f"File '{self.map_file}' is not found.We will load first map for you.")
            self.map_file = "move_map_1.json"
            self.map = Map(path.join(map_folder, self.map_file))

        # print(self.map.data)

    def _init_world(self, user_no: int):
        for i in range(user_no):
            world = Box2D.b2.world(gravity=(0, 0), doSleep=True, CollideConnected=False)
            self.worlds.append(world)

    def _is_game_end(self):
        if self.frame >= self.game_end_time or len(self.eliminated_user) == len(self.cars):
            for car in self.cars:
                if car not in self.eliminated_user and car.is_running:
                    car.end_frame = self.frame
                    self.eliminated_user.append(car)
                    self.user_check_points.append(car.check_point)
                    car.is_running = False
                    car.status = "GAME_OVER"
            self.is_end = True
            self.ranked_user = self.rank()
            self._print_result()
            self.status = "END"

    def draw_grid(self):
        for x in range(TILE_LEFTTOP[0], TILE_WIDTH + TILE_LEFTTOP[0], TILESIZE):
            pygame.draw.line(self.screen, GREY, (x, TILE_LEFTTOP[1]), (x, TILE_HEIGHT + TILE_LEFTTOP[1]))
        for y in range(TILE_LEFTTOP[1], TILE_HEIGHT + TILE_LEFTTOP[1], TILESIZE):
            pygame.draw.line(self.screen, GREY, (TILE_LEFTTOP[0], y), (TILE_WIDTH + TILE_LEFTTOP[0], y))
