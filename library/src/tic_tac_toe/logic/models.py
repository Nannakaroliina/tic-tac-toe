"""
Model class for Cross and Naught
"""
from __future__ import annotations

import enum
import re
import random

from dataclasses import dataclass
from functools import cached_property

from tic_tac_toe.logic.exceptions import InvalidMove, UnknownGameScore
from tic_tac_toe.logic.validators import validate_grid, validate_game_state

WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)


class Mark(str, enum.Enum):
    """
    Mark class for cross and naught string enum members.
    String enum is used so that we can compare the enum to string values.
    """
    CROSS = "X"
    NAUGHT = "O"

    @property
    def other(self) -> "Mark":
        """
        Returns the remaining free member of Mark, when one of them is already picked.
        :return: Remaining member of Mark
        """
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT


@dataclass(frozen=True)
class Grid:
    """
    Class that is used for the immutable tic-tac-toe grid.
    Does post initialization check to see if grid contains only valid values.
    """
    cells: str = " " * 9

    def __post_init__(self) -> None:
        validate_grid(self)

    @cached_property
    def x_count(self) -> int:
        """
        Count the amount of X's in the grid.
        :return: Total of X's as integer.
        """
        return self.cells.count("X")

    @cached_property
    def o_count(self) -> int:
        """
        Count the amount of 0's in the grid.
        :return: Total of 0's as integer.
        """
        return self.cells.count("O")

    @cached_property
    def empty_count(self) -> int:
        """
        Count the amount of spaces in the grid.
        :return: Total of spaces as integer.
        """
        return self.cells.count(" ")


@dataclass(frozen=True)
class Move:
    """
    Class that is used to define the players move and where the mark was placed.
    """
    mark: Mark
    cell_index: int
    before_state: "GameState"
    after_state: "GameState"


@dataclass(frozen=True)
class GameState:
    """
    Class that records the game state.
    """
    grid: Grid
    starting_mark: Mark = Mark("X")

    def __post_init__(self) -> None:
        validate_game_state(self)

    @cached_property
    def current_mark(self) -> Mark:
        """
        Checks the count of marks in grid and returns 0 or X based on the state of game.
        :return: Mark which turn it's to play
        """
        if self.grid.x_count == self.grid.o_count:
            return self.starting_mark
        else:
            return self.starting_mark.other

    @cached_property
    def game_not_started(self) -> bool:
        """
        Check whether the game has started or not. Returns True if game hasn't started yet.
        :return: True or false
        """
        return self.grid.empty_count == 9

    @cached_property
    def game_over(self) -> bool:
        """
        Check whether the game has finished or not.
        Returns true if there is winner or the game ends to tie.
        :return: True or false
        """
        return self.winner is not None or self.tie

    @cached_property
    def tie(self) -> bool:
        """
        Check whether the game ends to tie.
        Returns true if there isn't winner and grid has 0 empty cells.
        :return: True or false.
        """
        return self.winner is None and self.grid.empty_count == 0

    @cached_property
    def winner(self) -> Mark | None:
        """
        Check whether one of players has won.
        Compares the grid Marks to the winning patterns.
        :return: None or winning Mark.
        """
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return mark
        return None

    @cached_property
    def winning_cells(self) -> list[int]:
        """
        Check which cells led to winning the game.
        :return: Array of winning cells.
        """
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return [
                        match.start()
                        for match in re.finditer(r"\?", pattern)
                    ]
        return []

    @cached_property
    def possible_moves(self) -> list[Move]:
        """
        Check possible moves available.
        :return: Array of moves.
        """
        moves = []
        if not self.game_over:
            for match in re.finditer(r"\s", self.grid.cells):
                moves.append(self.make_move_to(match.start()))
        return moves

    def make_random_move(self) -> Move | None:
        """
        Make a random move to one of possible cells.
        :return: Move to valid cell.
        """
        try:
            return random.choice(self.possible_moves)
        except IndexError:
            return None

    def make_move_to(self, index: int) -> Move:
        """
        Checks if move is allowed and then takes the snapshot of player's move.
        :param index: index where the mark is placed.
        :return: Valid move
        """
        if self.grid.cells[index] != " ":
            raise InvalidMove("Cell is not empty")
        return Move(
            mark=self.current_mark,
            cell_index=index,
            before_state=self,
            after_state=GameState(
                Grid(
                    self.grid.cells[:index]
                    + self.current_mark
                    + self.grid.cells[index + 1:]
                ),
                self.starting_mark,
            ),
        )

    def evaluate_score(self, mark: Mark) -> int:
        """
        Check whether the game is over or not.
        0 is for game ending to tie.
        1 is for player winning the game.
        -1 is for player losing.
        :param mark: Current player's mark.
        :return: Int corresponding the game state.
        """
        if self.game_over:
            if self.tie:
                return 0
            if self.winner is mark:
                return 1
            else:
                return -1
        raise UnknownGameScore("Game is not over yet")
