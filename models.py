import enum
import random

class Cell:
    """
    An individual cell in the grid, which may or may not contain a mine,
    and is either covered, uncovered or flagged.
    """

    def __init__(self, mined=False):
        self.state = CellState.COVERED
        self.mined = mined


class CellState(enum.Enum):
    """Enum for the state of a Cell"""

    COVERED = enum.auto()
    UNCOVERED = enum.auto()
    FLAGGED = enum.auto()


class Grid:
    """A grid of Cells."""

    GRID_ROWS = 10
    GRID_COLUMNS = 10

    def __init__(self):
        # Create a GRID_ROWS x GRID_COLUMNS grid of Cells in their
        # default state
        self._grid = []
        for i in range(self.GRID_ROWS):
            row = []
            for j in range(self.GRID_COLUMNS):
                row.append(Cell())

            self._grid.append(row)
        
        # Initialise the mine positions
        self._set_mines()
    
    def __str__(self):
        """
        Get a console-friendly string representation of the grid with
        row and column indexes.
        """
        COLUMN_WIDTH = 1
        COVERED_CELL = " "
        FLAGGED_CELL = "F"
        MINED_CELL = "*"
        NO_NEIGHBOUR_MINES = "."
        COLUMN_DIVIDER = "|"

        stringrepr = ""

        # Add column indexes
        stringrepr += " " * (COLUMN_WIDTH + 2)
        for i in range(self.GRID_COLUMNS):
            stringrepr += str(i).ljust(COLUMN_WIDTH + 1)
        stringrepr += "\n"
        
        # Horizontal line
        for i in range(self.GRID_COLUMNS + 1):
            stringrepr += "-" * (COLUMN_WIDTH + 1)
        stringrepr += "\n"
        
        # Add each row of the grid
        for row in range(len(self._grid)):
            # Row index label
            stringrepr += str(row).ljust(COLUMN_WIDTH + 1) + COLUMN_DIVIDER

            # Add each cell in the row
            for col in range(len(self._grid[row])):
                cell = self._grid[row][col]

                if cell.state == CellState.COVERED:
                    stringrepr += COVERED_CELL
                elif cell.state == CellState.FLAGGED:
                    stringrepr += FLAGGED_CELL
                else:
                    # Cell is uncovered or in an invalid state
                    if cell.mined:
                        stringrepr += MINED_CELL
                    else:
                        # Display the number of surrounding Cells which
                        # contain mines
                        mined_neighbours = self._mined_neighbours(row, col)

                        if mined_neighbours == 0:
                            stringrepr += NO_NEIGHBOUR_MINES
                        else:
                            stringrepr += str(mined_neighbours)

                stringrepr += COLUMN_DIVIDER
            stringrepr += "\n"

        return stringrepr
    
    def _set_mines(self):
        """
        Set the Cells in the board which will contain mines. Intended
        to be called when a Grid is created.
        
        This method does not clear any positions which have already been
        set to have mines.
        """
        NUM_MINES = 10

        # Positions in the grid which will be set to have a mine, stored
        # as (row, col) tuples
        cells_to_mine = set()
        while len(cells_to_mine) < NUM_MINES:
            row = random.randrange(self.GRID_ROWS)
            col = random.randrange(self.GRID_COLUMNS)
            cells_to_mine.add((row, col))
        
        for cell_pos in cells_to_mine:
            self._grid[cell_pos[0]][cell_pos[1]].mined = True
    
    def _mined_neighbours(self, row, col):
        """
        Get the number of mined Cells that are neighbours of the Cell
        at (row, col)
        """
        mine_count = 0
        # Check all eight neighbouring cells of (col, row)
        for r in range(-1, 2):
            for c in range(-1, 2):
                # Skip the current cell and cells outside of the grid
                if (not (r == 0 and c == 0)
                    and self.has_cell_at(row + r, col + c)):
                    # Increment the mine counter if position is mined
                    if self._grid[row + r][col + c].mined:
                        mine_count += 1
        
        return mine_count
    
    def has_cell_at(self, row, col):
        """
        Return True if (row, col) is a valid position in the grid, i.e.
        0 <= row < GRID_ROWS and 0 <= col < GRID_COLUMNS.
        """
        return (row >= 0 and row < self.GRID_ROWS
                and col >= 0 and col < self.GRID_COLUMNS)
    
    def cell_state_at(self, row, col):
        """
        Get the state of the cell at (row, col), or None otherwise.
        """
        if self.has_cell_at(row, col):
            return self._grid[row][col].state
        else:
            return None
    
    def set_cell_state(self, row, col, new_state):
        """
        Set the cell at (row, col) to have state new_state.
        
        Returns False if the cell does not exist.
        """
        if self.has_cell_at(row, col):
            self._grid[row][col].state = new_state
            return True
        else:
            return False