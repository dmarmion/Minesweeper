from tkinter import *

from models import Grid

class GuiView:
    """GUI-based view for a minesweeper game."""
    
    def __init__(self):
        # The game this view is representing.
        # Must be set before many operations can take place
        self._game = None

        # Main window
        self._root = Tk()
        self._root.title("Minesweeper")

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
    
    def invalid_move(self):
        """Called when the player makes an invalid move."""
    
    def turn_started(self):
        """
        Called when a turn begins, before the user makes their move.
        """
    
    def mine_hit(self):
        """Called when a mine is hit."""
    
    def game_won(self):
        """Called when all non-mined cells have been uncovered."""
    
    def _create_widgets(self):
        """Create and add the widgets to the window."""
        # Create the grid
        grid_frame = LabelFrame(self._root, padx=8, pady=8)
        self._buttons = []

        for r in range(Grid.GRID_ROWS):
            row = []
            for c in range(Grid.GRID_COLUMNS):
                b = Button(grid_frame, padx=8)
                b.grid(row=r, column=c)

                row.append(b)
            self._buttons.append(row)
        
        grid_frame.grid(row=0, column=0)

        # Status bar
        self._status_bar = Label(self._root, text="Welcome to Minesweeper!")
        self._status_bar.grid(row=1, column=0)
        