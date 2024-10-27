from abc import ABC, abstractmethod

class Player(ABC):
    """Abstract Player class to define a common interface."""

    @abstractmethod
    def get_best_move(self):
        """Get the best move for the current game state."""
        pass
