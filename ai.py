##############################################################################
# FILE : ai.py
# WRITER : Jason Greenspan, jasonmg, 336126362; Yonatan Chamudot, ychamudot,
#  312516289
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION: Defines the AI class, which can play the four in a row game.
##############################################################################


from game import Game
import random
import copy

class AI:

    NUMBER_OF_CHOICES = Game.COLUMNS


    def __init__(self):
        """Initializes the AI class"""
        self.choices = self.NUMBER_OF_CHOICES

    def find_legal_move(self, g, func, timeout=None):
        """Take a Game object and a function, check through a hierarchy of 
        potential moves to play. If one of them exists, play that move and 
        return the move."""
        if self.winning_move(g) is not None: #Checks if the ai can win with 
                                             # one move
            winning_move = self.winning_move(g)
            func(winning_move)
            return winning_move
        elif self.blocking_move(g) is not None: #Checks if the ai can 
            # prevent its opponent from winning with one move
            blocking_move = self.blocking_move(g)
            func(blocking_move)
            return blocking_move
        else: #At the most basic level, check if the ai can move randomly
            basic_move = self.basic_move(g)
            func(basic_move)
            return basic_move

    def winning_move(self, g):
        """Check if the ai can win with one move. If it can, return the move"""
        for move in range(self.choices):
            test_board = self.test_move(g, move)
            if g.check_winner_horizontal(test_board) or \
                    g.check_winner_vertical(test_board) or \
                    g.check_winner_diagonal(test_board):
                return move

    def blocking_move(self, g):
        """Check if the ai can block its opponent from winning in one move. 
        If it can, return the move."""
        for move in range(self.choices):
            test_board = self.test_move(g, move, True)
            if g.check_winner_horizontal(test_board) or \
                    g.check_winner_vertical(test_board) or \
                    g.check_winner_diagonal(test_board):
                if g.board[0][move] == g.BLANK:
                    return move

    def basic_move(self, g):
        """Check if the ai can move to a random column. If it can, return 
        the move"""
        move = random.choice(range(self.choices))
        if g.board[0][move] == g.BLANK:
            return move
        else:
            if g.number_of_moves == g.max_moves:
                raise Exception("No possible AI moves.")
            #move = self.basic_move(g)
            print(move)
            print("retry")
            return self.basic_move(g)

    def test_move(self, g, column, opponent=False):
        """Take a Game object, a column number, and a boolean representing 
        whether to check for the ai's pieces or its opponent's pieces. 
        Return a copy of the game board with the correct player's piece 
        played in the designated column."""
        test_board = copy.deepcopy(g.board)
        current_color = g.get_current_player()
        if opponent:
            if current_color == g.PLAYER_ONE:
                current_color = g.PLAYER_TWO
            elif current_color == g.PLAYER_TWO:
                current_color = g.PLAYER_ONE
        for row in range(g.ROWS):
            if test_board[row][column] != g.BLANK:
                if row != 0:
                    test_board[row - 1][column] = current_color
                    break
            else:
                if row == g.ROWS - 1:
                    test_board[row][column] = current_color
                else:
                    continue
        return test_board
