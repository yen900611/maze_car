import unittest
import unittest.mock

from game_core.MazeCar import MazeCar
from game_core.mazeMode import MazeMode
from game_core.sound_controller import SoundController

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.MLGame = unittest.mock.MagicMock()
        self.cmd = {"ml_1P": [{"left_PWM": 100, "right_PWM": 0}],
                "ml_2P": [{"left_PWM": 0, "right_PWM": 100}]}
        self.MLGame.update.return_value = self.cmd
        # self.MLGame.get_game_progress.return_value =
    def test_game_could_get_cmd(self):
        try:
            game = MazeCar(1, "MAZE",1, 15, "OFF")
            self.assertEqual(self.MLGame.update(), game.game_mode.command)
        except:
            self.fail()
        pass
    def test_mode_coould_get_cmd(self):
        try:
            sound_controller = SoundController("OFF")
            game = MazeMode(1, 1, 120, sound_controller = sound_controller)
            while game.isRunning():
                game.update_sprite(self.cmd)
                self.assertEqual(self.cmd, game.command)

        except Exception as e:
            print(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()
