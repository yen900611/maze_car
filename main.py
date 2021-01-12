import pygame
from game_core import sound_controller, playingMode, I_Commander

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    sound_controller = sound_controller.SoundController("OFF")
    game = playingMode.PlayingMode(1,1,110, "OFF")

    while game.isRunning():
        commands = {}
        for i in range(6):
            commands["ml_" + str(i+1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game.draw_bg()
        game.drawWorld()
        game.flip()

    pygame.quit()
