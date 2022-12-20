"""
Player module to provide human and computer player object for game.
"""
from __future__ import annotations

import abc
import time

from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.minimax import find_best_move
from tic_tac_toe.logic.models import GameState, Mark, Move


class Player(metaclass=abc.ABCMeta):
    """
    Player class for players of the game.
    """
    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    def make_move(self, game_state: GameState) -> GameState:
        """
        Make the move in the game.
        :param game_state: Current game state.
        :return: State after move.
        """
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("No more possible moves")
        else:
            raise InvalidMove("It's the other player's turn")

    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state."""


class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    """
    Computer player class to play against
    """
    def __init__(self, mark: Mark, delay_seconds: float = 0.25) -> None:
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        """
        Wait a certain time before making the computed move.
        :param game_state: Current game state.
        :return: Computer's move.
        """
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer's move in the given game state."""


class RandomComputerPlayer(ComputerPlayer):
    """
    Random computer player which makes a random pick for the move.
    """
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """
        Picks the random cell of possible cells and makes the move.
        :param game_state: Current game state.
        :return: Returns the picked move.
        """
        return game_state.make_random_move()


class MinimaxComputerPlayer(ComputerPlayer):
    """
    Minimax algorithm enhanced computer player for calculated game playing.
    Tried to find the best possible moves for the game.
    """
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """
        Function that makes random first move and then continues with calculated moves.
        :param game_state: Current game state.
        :return: Computer's move.
        """
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_move(game_state)
