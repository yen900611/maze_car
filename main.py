import pygame
from src import MazeCar

from src.env import FPS
from mlgame.view.view import PygameView
from mlgame.game.generic import quit_or_esc

SOUND_OFF = "off"

MOVE_MAZE = "MOVE_MAZE"

if __name__ == '__main__':
    pygame.init()
    # game = MazeCar.MazeCar(6, "MAZE", 6, 10000, 3, "off")
    # game = MazeCar.MazeCar(user_num=2, game_type=MOVE_MAZE, map=5, time_to_play=2000, sensor_num=3, sound=SOUND_OFF)
    game = MazeCar.MazeCar(2, "PRACTICE", 12, 10000, 5, "off")
    scene_init_info_dict = game.get_scene_init_data()
    game_view = PygameView(scene_init_info_dict)
    frame_count = 0
    while game.is_running and not quit_or_esc():
        pygame.time.Clock().tick_busy_loop(FPS)
        game.update(game.get_keyboard_command())
        game_progress_data = game.get_scene_progress_data()
        game_view.draw(game_progress_data)
        frame_count += 1

    pygame.quit()
