jasonmg,ychamudot
336126362,312516289
Jason Greenspan,Yonatan Chamudot
=========================================
=     README for ex12: Connect Four     =
=========================================

==================
=  Description:  =
==================
An implementation of the classic game connect four, including an AI and
communication abilities
AI class:
__init__(self):
        """Initializes the AI class"""
find_legal_move(self, g, func, timeout=None):
        """Take a Game object and a function, check through a hierarchy of
        potential moves to play. If one of them exists, play that move and
        return the move."""
winning_move(self, g):
        """Check if the ai can win with one move. If it can, return the move"""
blocking_move(self, g):
        """Check if the ai can block its opponent from winning in one move.
        If it can, return the move."""
basic_move(self, g):
        """Check if the ai can move to a random column. If it can, return
        the move"""
test_move(self, g, column, opponent=False):
        """Take a Game object, a column number, and a boolean representing
        whether to check for the ai's pieces or its opponent's pieces.
        Return a copy of the game board with the correct player's piece
        played in the designated column."""

Game Class:
__init__(self):
        """Initializes a Game object"""
make_move(self, column):
        """Take an int representing a column on the game board, and add a
        piece representing the current player's color to the column """
get_winner(self):
        """Check if the current game board contains four pieces of the same
        color in a row horizontally, vertically, or diagonally. Also checks
        if the game has ended in a draw. If there is a winner, return which
        player won, and if there is a draw return the DRAW constant"""
check_winner_horizontal(self, *args):
        """Checks if there is a winner horizontally. If there is, return True"""
check_winner_vertical(self, *args):
        """Check if there is a winner vertically. If there is, return True"""
check_winner_diagonal(self, *args):
        """Checks if there is a winner diagonally. If there is, return True"""
get_diagonals(self, *args):
        """Return a list of all the diagonal rows in a game board. Filters
        the list so that it includes only diagonals of length 4 or greater"""
get_player_at(self, row, col):
        """Take row and column coordinates and return the player whose piece
        is present at that location on the game board"""
get_current_player(self):
        """Return the current player"""
switch_player(self):
        """Switch the current player"""

GameBoard Class
__init__(self, root, game, ai, communicator, is_human, server_status):
        """Initializes the GameBoard class"""
__build_board(self):
        """Builds GUI of board (row of buttons and empty tiles) when
        GameBoard is initialized."""
__ai_turn(self):
        """If AI player is activated, makes move."""
__make_button(self, column_coord):
        """Adds piece to board if it is the turn of the player who pressed
        the button. Communicates that the piece was added and checks
        for winner."""
__mouse_on(self, column_coord):
        """Changes color of button if current player focuses on it."""
__mouse_off(self, column_coord):
        """Changes color of button back to original color when
         player leaves focuses on it."""
__update_board(self, column_coord):
        """Updates using game the location of added piece for player's
        choice. Adds appropriate piece to position in GUI."""
__next_move(self, is_turn):
        """Changes to next players turn and updates color of buttons
        accordingly."""
__end_game(self, winner):
        """Check for winner and end game if there is one (or draw)."""
__end_message(self, message, color="black"):
        """Display message at top of board in given color.
         Overwrites buttons place in top row."""
__handle_message(self, message):
        """Handles message from communicator: updates board,
        checks for winner, and prepares next move."""
check_args(args):
    """Checks system arguments for correct amount, values of is_human arg,
    and valid value for port arg. Raises exception if there is an error."""

======================
=  Special Comments  =
======================
AI strategy- Bonus
Our AI's strategy involves three steps. First the AI will check the board to
see if it can play a move that will win the game. If not, it will check the
board to see if there is a move that its opponent can make which will win the
game. If so, it will block that move. Lastly, if the AI can not play a winning
move or a blocking move, it will move to a random legal location.
