class ConsoleView:
    """Console-output view for a minesweeper game."""

    def __init__(self):
        # The game this view is representing.
        # Must be set before many operations can take place
        self._game = None
    
    def general_help_message(self):
        """Prints a general usage message."""
        print("Help:")
        print()
        print("There are four commands you can enter at each move:")
        print("'flag', 'uncover', 'help' and 'quit'.")
        print()
        print("flag: 'flag <column> <row>'")
        print("Mark a cell as containing a mine.")
        print()
        print("uncover: 'uncover <column> <row>'")
        print("Uncover a cell. Once uncovered, the cell will state how many neighbouring cells contain a mine.")
        print()
        print("help: 'help'")
        print("Diplays this message.")
        print()
        print("quit: 'quit'")
        print("Exits the game.")
        print()
    
    def invalid_move(self):
        """
        Called when the player makes an invalid move.

        Prints a brief overview of valid moves.
        """
        print("Sorry, I don't recognise that command.")
        print("The moves you can make are:")
        print(" - flag <column> <row>")
        print(" - uncover <column> <row>")
        print(" - help")
        print(" - quit")
        print()
        print("For more information, type 'help'")
        print()
    
    def invalid_flag_command(self):
        """
        Called when the player enters an incorrectly formatted flag
        command.
        """
        print("Sorry, the command you entered appears to be incorrectly formatted.")
        print("The expected format for flag commands is:")
        print("flag <column> <row>, e.g. 'flag 4 8'")
        print()

    def invalid_uncover_command(self):
        """
        Called when the player enters an incorrectly formatted uncover
        command.
        """
        print("Sorry, the command you entered appears to be incorrectly formatted.")
        print("The expected format for uncover commands is:")
        print("uncover <column> <row>, e.g. 'uncover 4 8'")
        print()

    def _board_updated(self):
        """Print the current state of the board"""
        if self._game is not None:
            print(self._game.grid)
    
    def game_started(self):
        """
        Called when the game begins.

        Prints a welcome message.
        """
        print("Welcome to Minesweeper!", end='\n\n')

    def turn_started(self):
        """
        Called when a turn begins, before the user enters their move.

        Prints the current game state and prompts the user to enter
        their move.
        """
        self._board_updated()
        
        # Print prompt for user input
        print("Please enter your move:")
        print("> ", end='')
    
    def mine_hit(self):
        """Called when a mine is hit."""
        self._board_updated()
        print("A mine was hit!")
        print("Game over.")
        print()
    
    def game_won(self):
        """Called when all non-mined cells have been uncovered."""
        self._board_updated()
        print("You win!")
        print()
    
    def cells_uncovered(self):
        """Called when cells have been uncovered in the grid."""
        # No-op for console view
