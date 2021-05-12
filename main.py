import pygame
from game_core import sound_controller, mazeMode, I_Commander, moveMazeMode, practiceMode
from game_core.gameView import PygameView
from game_core.game_object_data import *

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    sound_controller = sound_controller.SoundController("OFF")
    game = mazeMode.MazeMode(1, 4, 120, sound_controller)
    # game = moveMazeMode.MoveMazeMode(2, 6, 120, sound_controller)
    # game = practiceMode.PracticeMode(1, 5, 120, sound_controller)
    sound_controller.play_music()
    game_view = PygameView(get_scene_init_sample_data())

    while game.isRunning():
        commands = {}
        for i in range(6):
            commands["ml_" + str(i + 1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game_view.draw(get_progress_data(game))
        game_view.flip()

    pygame.quit()
