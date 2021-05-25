import pygame
from game_core import I_Commander, MazeCar

if __name__ == '__main__':
    pygame.init()
    game = MazeCar.MazeCar(1, "MOVE_MAZE", 3, 20, "OFF")

    while game.isRunning():
        commands = {}
        for i in range(6):
            commands["ml_" + str(i + 1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        game.update(commands)

    pygame.quit()
