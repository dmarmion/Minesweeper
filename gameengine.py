import time

from models import CellState, Grid

class GameEngine:
    """Model representing a game of Minesweeper"""

    def __init__(self, view):
        # Set up a game
        self.grid = Grid()
        self.game_over = False
        self.game_start_time = time.time()

        # View for presenting data to user
        self.view = view
        view._game = self
        view.game_started()
    
    def uncover_cell(self, row, col):
        """
        Uncover a Cell in the grid.
        
        Returns True if the cell exists and was previously in the
        covered state.
        """
        if not self.game_over:
            if (self.grid.has_cell_at(row, col)
                and self.grid.cell_state_at(row, col) == CellState.COVERED):
                # Uncover that cell, and any relevant neighbours that
                # should also be uncovered
                if not self.grid.uncover_from(row, col):
                    # A mine was hit
                    self.view.mine_hit()
                    self.game_over = True

                # Update the game-over status
                if not self.grid.cells_left_to_uncover():
                    self.game_over = True
                    self.view.game_won()
                
                return True
            else:
                return False
        else:
            # Game has already finished, no more moves can be made
            return False

    def flag_cell(self, row, col):
        """
        Flag a cell in the grid as containing a mine, or unflag it if
        that cell is already flagged.

        Returns True if the move was valid, i.e. the cell was covered.
        """
        if not self.game_over:
            # To be able to toggle the flag-state of the cell, it must
            # both exist and be in the COVERED or FLAGGED state
            if self.grid.has_cell_at(row, col):
                current_state = self.grid.cell_state_at(row, col)

                if current_state == CellState.COVERED:
                    self.grid.set_cell_state(row, col, CellState.FLAGGED)
                elif current_state == CellState.FLAGGED:
                    self.grid.set_cell_state(row, col, CellState.COVERED)
                else:
                    # Cannot flag uncovered cells
                    return False
            else:
                return False
        else:
            # Game has already finished, no more moves can be made
            return False