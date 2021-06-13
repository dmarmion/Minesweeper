import time

from models import CellState, Grid

class GameEngine:
    """Model representing a game of Minesweeper"""

    def __init__(self):
        # Set up a game
        self._grid = Grid()
        self.game_over = False
        self.game_start_time = time.time()
    
    def uncover_cell(self, row, col):
        """
        Uncover a Cell in the grid.
        
        Returns True if the cell exists and was previously in the
        covered state.
        """
        if not self.game_over:
            if (self._grid.has_cell_at(row, col)
                and self._grid.cell_state_at(row, col) == CellState.COVERED):
                # Uncover that cell, and if it has no mined neighbours,
                # keep uncovering cells until no more cells without
                # mined neighbours are uncovered.
                # TODO comment needs updating
                #
                #
                #
                if not self._grid.uncover_from(row, col):
                    # A mine was hit
                    # TODO
                    # print("Mine hit!")
                    pass

            else:
                return False
        else:
            # Game has already finished, no more moves can be made
            return False

    def flag_cell(self, row, col):
        """
        Flag a cell in the grid as containing a mine, or unflag it if
        that cell is alreafy flagged.

        Returns True if the move was valid, i.e. the cell was covered.
        """
        if not self.game_over:
            # To be able to toggle the flag-state of the cell, it must
            # both exist and be in the COVERED or FLAGGED state
            if self._grid.has_cell_at(row, col):
                current_state = self._grid.cell_state_at(row, col)

                if current_state == CellState.COVERED:
                    self._grid.set_cell_state(row, col, CellState.FLAGGED)
                elif current_state == CellState.FLAGGED:
                    self._grid.set_cell_state(row, col, CellState.COVERED)
                else:
                    # Cannot flag uncovered cells
                    return False
            else:
                return False
        else:
            # Game has already finished, no more moves can be made
            return False