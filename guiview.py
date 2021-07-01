from functools import partial
from tkinter import *

from models import CellState, Grid

BLANK_CELL = "  "

class GuiView:
    """GUI-based view for a minesweeper game."""
    
    def __init__(self):
        # The game this view is representing.
        # Must be set before many operations can take place
        self._game = None

        # Main window
        self._root = Tk()
        self._root.title("Minesweeper")
        self._root.resizable(False, False)

    def game_started(self):
        """
        Called when the game begins.
        
        Adds the widgets to the window and begins the main loop.
        """
        if self._game is not None:
            self._create_widgets()
        else:
            # Game was not set
            error_label = Label(
                self._root, text="An error occured while loading the game.")
            error_label.pack()

        self._root.mainloop()
    
    def cells_updated(self):
        """Called when cells have been uncovered in the grid."""
        self._update_grid()
    
    def mine_hit(self):
        """Called when a mine is hit."""
        self._set_status("You hit a mine. Game over.")
        self._disable_grid()        
    
    def game_won(self):
        """Called when all non-mined cells have been uncovered."""
        self._set_status("You win!")
        self._disable_grid()        
    
    def _create_widgets(self):
        """Create and add the widgets to the window."""
        # Grid of cells
        grid_frame = LabelFrame(self._root, padx=8, pady=8)
        self._buttons = []

        for r in range(Grid.GRID_ROWS):
            row = []
            for c in range(Grid.GRID_COLUMNS):
                b = Button(grid_frame, height=1, width=2, padx=4,
                           text=BLANK_CELL,
                           command=partial(self._game.uncover_cell, r, c))

                # When the button is right-clicked, flag the cell
                b.bind("<Button-3>", partial(self._flag_cell, r, c))
                
                b.grid(row=r, column=c)

                row.append(b)
            self._buttons.append(row)
        
        grid_frame.grid(row=0, column=0)

        # Status bar
        self._status_bar = Label(self._root, text="Welcome to Minesweeper!")
        self._status_bar.grid(row=1, column=0)
    
    def _flag_cell(self, row, col, event):
        """
        Instruct the game to flag a cell in the grid. This method should
        be called instead of calling GameEngine.flag_cell() directly so
        that only the row and column indexes are passed to the
        GameEngine, and not the event.

        This method only forwards the call to the GameEngine - the
        updating of a flagged cell's appearance happens in
        GuiView._update_grid()
        """
        if self._game is not None:
            self._game.flag_cell(row, col)
    
    def _update_grid(self):
        """Update the state of the buttons in the grid."""
        for r in range(len(self._buttons)):
            for c in range(len(self._buttons[r])):
                btn = self._buttons[r][c]
                grid = self._game.grid

                if grid.cell_state_at(r, c) == CellState.UNCOVERED:
                    if grid.has_mine_at(r, c):
                        # (c, r) contains a mine
                        btn["bg"] = "red"
                        btn["fg"] = "black"
                        btn["text"] = "*"
                    else:
                        # (c, r) does not contain a mine
                        btn["bg"] = "#BDBDBD"
                        btn["fg"] = "black"

                        # Button text states how many neighbouring cells
                        # have mines, or is blank if that number is 0
                        mneighbours = grid.mined_neighbours(r, c)
                        if mneighbours > 0:
                            btn["text"] = mneighbours
                        
                elif grid.cell_state_at(r, c) == CellState.FLAGGED:
                    btn["fg"] = "red"
                    btn["text"] = "🚩"
                else:
                    # Cell is covered; resetting the text is necessary
                    # so that a cell returns to blank if it is unflagged
                    btn["text"] = BLANK_CELL
    
    def _disable_grid(self):
        """Disable all buttons in the grid."""
        for r in range(len(self._buttons)):
            for c in range(len(self._buttons[r])):
                self._buttons[r][c]["state"] = "disabled"

    def _set_status(self, message):
        """Display the given message in the status bar."""
        if self._status_bar is not None:
            self._status_bar["text"] = message