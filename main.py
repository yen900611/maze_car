import pygame
from game_core import sound_controller, mazeMode, I_Commander, moveMazeMode

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    sound_controller = sound_controller.SoundController("OFF")
    # game = mazeMode.MazeMode(2, 6, 20, sound_controller)
    game = moveMazeMode.MoveMazeMode(1, 1, 40, sound_controller)
    # game = collideMazeMode.CollideMode(1, 1, 110, sound_controller)
    sound_controller.play_music()

    while game.isRunning():
        commands = {}
        for i in range(6):
            commands["ml_" + str(i + 1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        # print(commands)
        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game.draw_bg()
        game.drawWorld()
        # game.all_sprites.draw(game.screen)
        game.flip()

    pygame.quit()
