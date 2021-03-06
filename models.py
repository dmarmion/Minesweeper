import enum
import random
import sys

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

    GRID_ROWS = 16
    GRID_COLUMNS = 16
    NUM_MINES = 40

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
        # Escape codes for coloured text
        RED_TEXT = "\033[91m"
        RESET_TEXT = "\033[00m"

        COLUMN_WIDTH = 1
        COVERED_CELL = " "
        FLAGGED_CELL = "F"
        MINED_CELL = "*"
        NO_NEIGHBOUR_MINES = "."
        COLUMN_DIVIDER = "|"

        # Make flags red unless -w is given as an argument
        if "-w" not in sys.argv:
            FLAGGED_CELL = RED_TEXT + FLAGGED_CELL + RESET_TEXT

        stringrepr = ""

        # Add column indexes
        stringrepr += " " * (COLUMN_WIDTH + 2)
        for i in range(self.GRID_COLUMNS):
            stringrepr += str(i).ljust(COLUMN_WIDTH + 1)
        stringrepr += "\n"
        
        # Horizontal line
        for i in range(self.GRID_COLUMNS + 1):
            stringrepr += "-" * (COLUMN_WIDTH + 1)
        stringrepr += "-\n"
        
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
                        mined_neighbours = self.mined_neighbours(row, col)

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
        # Positions in the grid which will be set to have a mine, stored
        # as (row, col) tuples
        cells_to_mine = set()
        while len(cells_to_mine) < self.NUM_MINES:
            row = random.randrange(self.GRID_ROWS)
            col = random.randrange(self.GRID_COLUMNS)
            cells_to_mine.add((row, col))
        
        for cell_pos in cells_to_mine:
            self._grid[cell_pos[0]][cell_pos[1]].mined = True
    
    def _neighbours_of(self, row, col):
        """Get a set of the cells that neighbour (row, col)."""
        neighbour_set = set()

        # Check all eight neighbouring positions of (col, row)
        for r in range(-1, 2):
            for c in range(-1, 2):
                # Skip the current cell and cells outside of the grid
                if (not (r == 0 and c == 0)
                    and self.has_cell_at(row + r, col + c)):
                    # Add the neighbur to the set
                    neighbour_set.add(self._grid[row + r][col + c])

        return neighbour_set

    def mined_neighbours(self, row, col):
        """
        Get the number of mined cells that are neighbours of the cell
        at (col, row)
        """
        mine_count = 0

        for neighbour in self._neighbours_of(row, col):
            if neighbour.mined:
                mine_count += 1
        
        return mine_count
    
    def has_cell_at(self, row, col):
        """
        Return True if (col, row) is a valid position in the grid, i.e.
        0 <= row < GRID_ROWS and 0 <= col < GRID_COLUMNS.
        """
        return (row >= 0 and row < self.GRID_ROWS
                and col >= 0 and col < self.GRID_COLUMNS)
    
    def has_mine_at(self, row, col):
        """
        Return True if (col, row) is a valid position in the grid and
        contains a mine.
        """
        if self.has_cell_at(row, col) and self._grid[row][col].mined:
            return True
        
        # Return false otherwise
        return False
    
    def cell_state_at(self, row, col):
        """
        Get the state of the cell at (col, row), or None otherwise.
        """
        if self.has_cell_at(row, col):
            return self._grid[row][col].state
        else:
            return None
    
    def set_cell_state(self, row, col, new_state):
        """
        Set the cell at (col, row) to have state new_state.
        
        Returns False if the cell does not exist.
        """
        if self.has_cell_at(row, col):
            self._grid[row][col].state = new_state
            return True
        else:
            return False
    
    def uncover_from(self, row, col):
        """
        Begin uncovering cells from (col, row).

        If (col, row) is not a mine, it's non-mine neighbours will be
        uncovered. Every time a neighbour cell with no neighbouring
        mines is uncovered, it's neighbours will also be uncovered.

        Returns True unless there is a mine at (col, row).
        """
        if self.has_cell_at(row, col):            
            if self._grid[row][col].mined:
                # Hit a mine - game over
                self._grid[row][col].state = CellState.UNCOVERED
                return False
            else:
                # No mine at (row, col)
                if self._grid[row][col].state == CellState.COVERED:
                    # Uncover (row, col)
                    self._recursively_uncover_from(row, col, set())
        
        # Always returns True unless a mine is hit
        return True

    def _recursively_uncover_from(self, row, col, visited_cells):
        """
        Implements the recursive cell uncovering component of
        Grid.uncover_from()

        Takes a cell, uncovers it and its neighbours (if reasonable
        to do so), then uncovers from any just-uncovered neighbours
        that neighbour 0 mined cells and are not mined themselves.

        Takes a set of cells already uncovered from to avoid infinte
        loops.
        """
        if self.has_cell_at(row, col):
            if (self._grid[row][col].state != CellState.FLAGGED
                and not self._grid[row][col].mined):
                # Uncover the cell and note that it's been visited
                self._grid[row][col].state = CellState.UNCOVERED
                visited_cells.add(self._grid[row][col])

                neighbours = self._neighbours_of(row, col)

                # Uncover each non-mine covered neighbour
                for neighbour in neighbours:
                    if (not (neighbour.mined
                        or neighbour.state == CellState.FLAGGED)):
                        # Uncover the neighbour
                        neighbour.state = CellState.UNCOVERED

                # For each neighbour with no mined neighbours, keep
                # uncovering from there
                for r in range(-1, 2):
                    for c in range(-1, 2):
                        # Skip the current cell and cells outside of the
                        # grid
                        if (not (r == 0 and c == 0)
                            and self.has_cell_at(row + r, col + c)):
                            # If the neighbour doesn't neighbour any
                            # mines, uncover from there
                            if (self.mined_neighbours(row + r, col + c) == 0
                                and (self._grid[row + r][col + c]
                                     not in visited_cells)):
                                self._recursively_uncover_from(row + r,
                                                               col + c,
                                                               visited_cells)

    def cells_left_to_uncover(self):
        """
        Check whether or not there are non-mined cells that haven't been
        uncovered yet.
        """
        # Count uncovered cells in grid
        uncovered_cells = 0
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLUMNS):
                if (self._grid[row][col].state == CellState.UNCOVERED
                    and not self._grid[row][col].mined):
                    # Increment counter
                    uncovered_cells += 1
        
        # Count mines in the grid
        mined_cells = 0
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLUMNS):
                if self._grid[row][col].mined:
                    mined_cells += 1
        
        # Calculate remaining non-mined covered cells
        remaining = (self.GRID_ROWS * self.GRID_COLUMNS
                    - mined_cells
                    - uncovered_cells)
        
        return remaining > 0
