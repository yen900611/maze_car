import unittest

from game_core.mazeMode import MazeMode


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        is_completed = [True, False, True, False, False]
        end_frame = [90, 100, 90, 100, 100]
        check_points = [6, 4, 6, 6, 1]
        self.game = MazeMode(5, 5, 2, "OFF")
        for car in self.game.cars:
            car.is_completed = is_completed[car.car_no]
            car.end_frame = end_frame[car.car_no]
            car.check_point = check_points[car.car_no]
            self.game.eliminated_user.append(car)

    def test_something(self):
        result = []
        same_rank = []
        for rank in self.game.rank():
            same_rank = []
            for user in rank:
                same_rank.append(user.car_no)
            result.append(same_rank)
        self.assertEqual(result, [[0, 2], [3], [1], [4]])


if __name__ == '__main__':
    unittest.main()
