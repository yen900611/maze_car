import unittest

from game_core.mazeMode import MazeMode


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        is_completed = [True, True, True, True, True]
        end_frame = [364, 851, 951, 752, 416]
        check_points = [7, 7, 7, 7, 7]
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
            for user in rank:
                same_rank.append(user.car_no)
            result.append(same_rank)
        self.assertEqual(result, [[0, 4, 3, 1, 2]])


if __name__ == '__main__':
    unittest.main()
