import unittest

from mlgame.view.view import PygameView


class MyTestCase(unittest.TestCase):
    def test_view_could_draw(self):
        try:
            game_info = {"images":
                             ["car0.png", "car_02.png", "car_03.png", "car_04.png", "car_05.png", "car_06.png", "info.png",]
                        }
            view = PygameView(game_info)
            data = {
                    "scene":{},
                    "game_object":[
                        {"type":"image",
                         "name":"car",
                         "coordinate":(10,20),
                         "size":(50,50),
                         "image":"car0.png",
                         "angle":260},
                        {"type":"rectangle",
                         "name":"ball",
                         "coordinate":(50,90),
                         "size":(5,5),
                         "color":(0,0,230)},
                        {"type":"vertices",
                         "name":"wall",
                         "coordinate":(80,60),
                         "color":(180,0,0),
                         "vertices":[(10,1),(3,1),(3,20),(10,20)]
                         }
                    ]
                }
            view.draw(data)
            view.flip()
        except Exception as e :
            print(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()
