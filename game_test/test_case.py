import unittest
import time

def count_position(vertices):
    v_sum = [0,0]
    for v in vertices:
        v_sum[0] += v[0]
        v_sum[1] += v[1]
    position = v_sum[0] / 4, v_sum[1] / 4
    return position
# def rank(time):
#     result = []
#     for i in range(len(time)):
#         if time[i] == time[i - 1]:
#             if i == 0:
#                 result.append(6)
#             else:
#                 for j in range(1,i + 1):
#                     if time[i - j] == time[i]:
#                         if i == j:
#                             result.append(6)
#                         else:
#                             pass
#                         pass
#                     else:
#                         result.append(6 - (i - j + 1))
#                         break
#         else:
#             result.append(6 - i)
#             pass
#     print(result)
#     return result

def ranking_score(score):
    ranked_player = []
    scores = []
    result = []
    for key in score.keys():
        scores.append(score[key])
        '''
        scores = [p1_score,p2_score....,p6_score]
        '''
    while len(scores) != 0:
        for key in score.keys():
            try:
                if score[key] == max(scores):
                    ranked_player.append(key)
                    scores.remove(score[key])
            except ValueError:
                pass
        '''
        ranked_player=[2P,3P,5P,1P,6P,4P] # sort from most score
        '''
    for i in range(len(ranked_player)):
        same_rank = []
        if i == len(ranked_player)-1:
            same_rank.append(ranked_player[i])
            result.append(same_rank)
        elif score[ranked_player[i]] == score[ranked_player[i - 1]]:
            pass
        elif score[ranked_player[i]] == score[ranked_player[i + 1]]:
            same_rank.append(ranked_player[i])
            for j in range(1,len(ranked_player)-i):

                if score[ranked_player[i + j]] == score[ranked_player[i]]:
                    if j == 0:
                        pass
                    else:
                        same_rank.append(ranked_player[i+j])
                        continue
                    break
                else:
                    break
            result.append(same_rank)

        else:
            same_rank.append(ranked_player[i])
            result.append(same_rank)
    return result


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.start_time = time.time()
        self.car_end_time = [[14, 15, 15], [15, 15, 15], [12, 13, 14, 14, 15], [3, 3, 4, 4, 5], [8, 8], [7],
                             [52, 73, 73, 98, 100, 100], [2, 2, 2, 2, 2, 2]]
        self.ranking_ans = [[6, 5, 5], [6, 6, 6], [6, 5, 4, 4, 2], [6, 6, 4, 4, 2], [6, 6], [6], [6, 5, 5, 3, 2, 2],
                            [6, 6, 6, 6, 6, 6]]
        self.score = [{"1P": 6, "2P": 5, "3P": 4, "4P": 3, "5P": 2, "6P": 1},
                      {"1P": 2, "2P": 1, "3P": 4, "4P": 3, "5P": 6, "6P": 5},
                      {"1P": 6, "2P": 6, "3P": 4, "4P": 3, "5P": 2, "6P": 1},
                      {"1P": 6, "2P": 5, "3P": 5, "4P": 3, "5P": 2, "6P": 1},
                      {"1P": 6, "2P": 5, "3P": 5, "4P": 5, "5P": 2, "6P": 1},
                      {"1P": 6, "2P": 5, "3P": 0, "4P": 0, "5P": 0, "6P": 0}]
        self.ans = [[["1P"], ["2P"], ["3P"], ["4P"], ["5P"], ["6P"]], [["5P"], ["6P"], ["3P"], ["4P"], ["1P"], ["2P"]],
                    [["1P", "2P"], ["3P"], ["4P"], ["5P"], ["6P"]],
                    [["1P"], ["2P", "3P"], ["4P"], ["5P"], ["6P"]],
                    [["1P"], ["2P", "3P","4P"], ["5P"], ["6P"]],
                    [["1P"], ["2P"], ["3P","4P", "5P", "6P"]]]
        self.vertices = [(1, 1), (19, 1), (1, 1.5), (19, 1.5)]
        self.positions = (10,1.25)

    # def test_time(self):
    #     now_time = self.start_time + 60.32
    #     self.assertEqual(self.game_mode.draw_time(now_time), [1,0,32])
    #
    # def test_maze(self):
    #     wall_vertices = []
    #     for wall in self.Maze[0]:
    #         vertices = []
    #         for vertice in wall:
    #             vertices.append((vertice[0]*20, 520 - vertice[1]*20))
    #         wall_vertices.append(vertices)
    #     self.assertEqual(wall_vertices, [[(20,500),(500,500),(20,490),(500,490)]])

    # def test_rank(self):
    #     for i in range(len(self.car_end_time)):
    #         self.assertEqual(rank(self.car_end_time[i]),self.ranking_ans[i])
    #     pass

    def test_ranking(self):
        for i in range(len(self.score)):
            self.assertEqual(self.ans[i], ranking_score(self.score[i]))
        pass
    def test_count_position(self):
        self.assertEqual(count_position(self.vertices), self.positions)


if __name__ == '__main__':
    unittest.main()
