from os import path
from .src.MazeCar import MazeCar
from mlgame.utils.parse_config import read_json_file, parse_config
from argparse import ArgumentTypeError

# test to push
# test to push again
# test to push and build
# test to push , build and run
# def positive_int(string):
#     value = int(string)
#     if value < 1:
#         raise ArgumentTypeError()
#     return value

config_file = path.join(path.dirname(__file__), "game_config.json")

config_data = read_json_file(config_file)
GAME_VERSION = config_data["version"]
GAME_PARAMS = parse_config(config_data)


GAME_SETUP = {
    "game": MazeCar,

    "ml_clients": [
        {"name": "ml_1P", "args": ("player1",)},
        {"name": "ml_2P", "args": ("player2",)},
        {"name": "ml_3P", "args": ("player3",)},
        {"name": "ml_4P", "args": ("player4",)},
        {"name": "ml_5P", "args": ("player5",)},
        {"name": "ml_6P", "args": ("player6",)},
    ],
    "dynamic_ml_clients":True
}
