from consoleview import ConsoleView
from gameengine import GameEngine

def main():
    """
    Run a game of Minesweeper using the console for output.
    Program ends when game ends.
    """
    # Set up game
    view = ConsoleView()
    game = GameEngine(view)

    # Game loop
    while not game.game_over:
        view.turn_started()

        # Get move to make from user and execute it
        move = input()
        print()
        
        execute_move(move, view)

        # Temp TODO remove
        game.game_over = True
    
def execute_move(move, view):
    """
    Take a raw user input, convert it to a move and execute that move.

    Valid moves are:
     - flag <position>    -- flag a position in the grid
     - uncover <position> -- uncover a position in the grid
     - help               -- display what moves are available
     - quit               -- quits the game
    
    A position is given as 'col row', where col and row are integers
    separated by one space, e.g. '4 8' corresponds to the cell in
    column 4 and row 8.
    """
    tokens = move.split()

    if len(tokens) > 0:
        command = tokens[0].lower()

        if command == "flag":
            pass
        elif command == "uncover":
            pass
        elif command == "help":
            pass
        elif command == "quit":
            pass
        else:
            # Unrecognised command
            view.invalid_move()
    else:
        view.invalid_move()

if __name__ == "__main__":
    main()