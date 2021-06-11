import time

from models import Grid

class GameEngine:
    """Model representing a game of Minesweeper"""

    def __init__(self):
        # Set up a game
        self._grid = Grid()
        self.game_over = True
        self.game_start_time = time.time()
    
    def uncover_cell(self, row, col):
        """Uncover a Cell in the grid."""
        pass

    def flag_cell(self, row, col):
        """Flag a cell in the grid as containing a mine."""
        pass