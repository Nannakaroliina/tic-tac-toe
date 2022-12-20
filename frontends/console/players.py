"""
Module that provides player classes for console.
"""
from __future__ import annotations

import re

from tic_tac_toe.game.players import Player
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Move


class ConsolePlayer(Player):
    """
    Interactive console player
    """
    def get_move(self, game_state: GameState) -> Move | None:
        """
        While game is ongoing, get the user's move.
        :param game_state: Current game state.
        :return: Move if valid.
        """
        while not game_state.game_over:
            try:
                index = grid_to_index(input(f"{self.mark}'s move: ").strip())
            except ValueError:
                print("Please provide coordinates in the form of A1 or 1A")
            else:
                try:
                    return game_state.make_move_to(index)
                except InvalidMove:
                    print("That cell is already occupied.")
        return None


def grid_to_index(grid: str) -> int:
    """
    Convert the user text input to numeric index.
    :param grid: Input grid.
    :return: Corresponding index in cells.
    """
    if re.match(r"[abcABC][123]", grid):
        col, row = grid
    elif re.match(r"[123][abcABC]", grid):
        row, col = grid
    else:
        raise ValueError("Invalid grid coordinates")
    return 3 * (int(row) - 1) + (ord(col.upper()) - ord("A"))
