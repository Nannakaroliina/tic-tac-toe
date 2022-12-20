"""
Validators used for the game.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tic_tac_toe.logic.models import Grid, GameState, Mark
    from tic_tac_toe.game.players import Player

import re

from tic_tac_toe.logic.exceptions import InvalidGameState


def validate_grid(grid: Grid) -> None:
    """
    Validate the grid cells that they contain only allowed characters:
    X, 0 or space (empty cell).
    :param grid: Grid object
    """
    if not re.match(r"^[\sXO]{9}$", grid.cells):
        raise ValueError("Must contain 9 cells of: X, O, or space")


def validate_game_state(game_state: GameState) -> None:
    """
    Validates the game state that there is proper number of marks,
    proper starting mark and proper winner.
    :return:
    """
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.starting_mark)
    validate_winner(
        game_state.grid, game_state.starting_mark, game_state.winner
    )


def validate_number_of_marks(grid: Grid) -> None:
    """
    Checks that the number of marks is correct.
    If amount of mark is greater than 1, raises an error.
    :param grid: Grid object
    """
    if abs(grid.x_count - grid.o_count) > 1:
        raise InvalidGameState("Wrong number of Xs and Os")


def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
    """
    Checks if the starting mark is right by comparing the amount of marks.
    :param grid: Grid object
    :param starting_mark: Mark that starts the game
    """
    if grid.x_count > grid.o_count:
        if starting_mark != "X":
            raise InvalidGameState("Wrong starting mark")
    elif grid.o_count > grid.x_count:
        if starting_mark != "O":
            raise InvalidGameState("Wrong starting mark")


def validate_winner(grid: Grid, starting_mark: Mark, winner: Mark | None) -> None:
    """
    Checks the mark counts and validates the winner.
    :param grid: Grid object
    :param starting_mark: Mark that starts the game
    :param winner: Winner mark
    """
    if winner == "X":
        if starting_mark == "X":
            if grid.x_count <= grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
        else:
            if grid.x_count != grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
    elif winner == "O":
        if starting_mark == "O":
            if grid.o_count <= grid.x_count:
                raise InvalidGameState("Wrong number of Os")
        else:
            if grid.o_count != grid.x_count:
                raise InvalidGameState("Wrong number of Os")


def validate_players(player1: Player, player2: Player) -> None:
    """
    Validate that the users are valid and using different marks.
    :param player1: Player object.
    :param player2: Player object.
    """
    if player1.mark is player2.mark:
        raise ValueError("Players must use different marks")
