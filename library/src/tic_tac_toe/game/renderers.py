"""
Renderer for the front.
"""
import abc

from tic_tac_toe.logic.models import GameState


class Renderer(metaclass=abc.ABCMeta):
    """
    Abstract renderer class for grid rendering.
    """
    @abc.abstractmethod
    def render(self, game_state: GameState) -> None:
        """Render the current game state."""
