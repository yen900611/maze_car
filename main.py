import pygame
from game_core import I_Commander, MazeCar, gameView

if __name__ == '__main__':
    pygame.init()
    game = MazeCar.MazeCar(1, "MAZE", 3, 1, "OFF")
    # game = MazeCar.MazeCar(1, "MOVE_MAZE", 3, 1, "OFF")
    # game = MazeCar.MazeCar(1, "PRACTICE", 3, 2, "OFF")
    scene_init_info_dict = game.get_game_info()
    game_view = gameView.PygameView(scene_init_info_dict)

    while game.isRunning():
        commands = {}
        for i in range(6):
            commands["ml_" + str(i + 1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        game.update(commands)
        game_progress_data = game.get_game_progress()
        game_view.draw_screen()
        game_view.draw(game_progress_data)
        game_view.flip()

    pygame.quit()
