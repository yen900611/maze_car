import pygame
from game_core import sound_controller, mazeMode, I_Commander, moveMazeMode

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    sound_controller = sound_controller.SoundController("ON")
    # game = mazeMode.PlayingMode(1, 1, 120, sound_controller)
    game = moveMazeMode.MoveMazeMode(1, 2, 40, "OFF")
    # game = collideMazeMode.CollideMode(1, 1, 110, "OFF")
    sound_controller.play_music()

    while game.isRunning():
        commands = {}
        for i in range(6):
            commands["ml_" + str(i + 1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game.draw_bg()
        game.drawWorld()
        game.flip()

    pygame.quit()
