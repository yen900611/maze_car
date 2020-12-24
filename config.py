GAME_VERSION = "1.1"

from argparse import ArgumentTypeError

# test to push
# test to push again
# test to push and build
# test to push , build and run
def positive_int(string):
    value = int(string)
    if value < 1:
        raise ArgumentTypeError()
    return value


GAME_PARAMS = {
    "()": {
        "prog": "Maze_Car",
        "game_usage": "%(prog)s <user_num> [game_type]"
    },
    "user_num": {
        "type": positive_int,
        "default": 3,
        "help": ("[Optional] The score that the game will be exited "
                 "when either side reaches it.[default: %(default)s]")
    },
    "game_type": {
        "choices": ("NORMAL"),
        "metavar": "difficulty",
        "nargs": "?",
        "default": "NORMAL",
        "help": "Specify the game style. Choices: %(choices)s"
    },
    "Maze": {
        "type": positive_int,
        "default": 1,
        "help": "Specify the game style. Choices: %(choices)s"
    },
    "sound":{
        "choices":("on","off"),
        "default":"off"
    }
}

from .game_core.MazeCar import MazeCar

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
