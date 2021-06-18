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
        
        execute_move(move, game, view)

        # Temp TODO remove
        game.game_over = True
    
    # print(game.grid)
    
def execute_move(move, game, view):
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
            # Flag commands are expected to be in the format
            # 'flag <col> <row>'
            if len(tokens) == 3:
                try:
                    col = int(tokens[1])
                    row = int(tokens[2])

                    game.flag_cell(row, col)
                except ValueError:
                    view.invalid_flag_command()
            else:
                view.invalid_flag_command()

        elif command == "uncover":
            # Uncover commands are expected to be in the format
            # 'uncover <col> <row>'
            if len(tokens) == 3:
                try:
                    col = int(tokens[1])
                    row = int(tokens[2])

                    game.uncover_cell(row, col)
                except ValueError:
                    view.invalid_uncover_command()
            else:
                view.invalid_uncover_command()

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