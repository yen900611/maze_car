import pygame
from game_core import MazeCar,  I_Commander
from game_test import game_test

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    game = game_test.MazeCar(2, "MAZE", 1, 120, "OFF")
    # game = game_test.MazeCar(2, "MOVE_MAZE", 1, 12., "OFF")
    # sound_controller.play_music()

    while game.isRunning():
        cmd = {}
        for i in range(6):
            cmd["ml_" + str(i + 1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        # cmd = game.get_keyboard_command()
        # print(cmd)
        game.update(cmd)

    pygame.quit()