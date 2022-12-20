"""
Front end renderers for the game grid.
"""
import textwrap

from typing import Iterable

from tic_tac_toe.game.renderers import Renderer
from tic_tac_toe.logic.models import GameState


class ConsoleRenderer(Renderer):
    """
    Console renderer to render the game to console.
    """
    def render(self, game_state: GameState) -> None:
        """
        Clean the screen for new game and print the grid.
        If there is a winner, blink effect is used plus winner printed.
        :param game_state: Current game state.
        """
        clear_screen()
        if game_state.winner:
            print_blinking(game_state.grid.cells, game_state.winning_cells)
            print(f"{game_state.winner} wins \N{party popper}")
        else:
            print_solid(game_state.grid.cells)
            if game_state.tie:
                print("No one wins this time \N{neutral face}")


def clear_screen() -> None:
    """
    Reset the console to clear.
    """
    print("\033c", end="")


def blink(text: str) -> str:
    """
    Blink state to clarify who won the game.
    :param text: The marks string.
    :return: Returns blinking text.
    """
    return f"\033[5m{text}\033[0m"


def print_blinking(cells: Iterable[str], positions: Iterable[int]) -> None:
    """
    Prints the grid with blinking winner marks.
    :param cells: Sequence of cells.
    :param positions: Sequence of winning mark positions.
    """
    mutable_cells = list(cells)
    for position in positions:
        mutable_cells[position] = blink(mutable_cells[position])
    print_solid(mutable_cells)


def print_solid(cells: Iterable[str]) -> None:
    """
    Print the grid for the game
    :param cells: Sequence of cells
    """
    print(
        textwrap.dedent(
            """\
             A   B   C
           ------------
        1 ┆  {0} │ {1} │ {2}
          ┆ ───┼───┼───
        2 ┆  {3} │ {4} │ {5}
          ┆ ───┼───┼───
        3 ┆  {6} │ {7} │ {8}
    """
        ).format(*cells)
    )