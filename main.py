
if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    sound_controller = sound_controller.SoundController("off")

    while game.isRunning():
        commands = {}
        for i in range(4):
            commands["ml_" + str(i+1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()
        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game.draw_bg()
        game.drawAllSprites()
        game.flip()

    pygame.quit()
