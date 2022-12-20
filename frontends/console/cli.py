"""
Module for cli.
"""
from tic_tac_toe.game.engine import TicTacToe

from .args import parse_args
from .renderers import ConsoleRenderer


def main() -> None:
    """
    Class that parses the command-line arguments and returns start state for game.

    Run the game for two human players by following commands:
    (venv) $ cd frontends/
    (venv) $ python -m console -X human -O human

    Human vs computer with random moves:
    (venv) $ python -m console -X minimax -O minimax

    AI vs AI:
    (venv) $ python -m console -X minimax -O minimax
    """
    player1, player2, starting_mark = parse_args()
    TicTacToe(player1, player2, ConsoleRenderer()).play(starting_mark)