from game import Game
import random
import copy

class AI:

    NUMBER_OF_CHOICES = Game.COLUMNS


    def __init__(self):
        self.choices = self.NUMBER_OF_CHOICES

    def find_legal_move(self, g, func, timeout=None):
        if self.winning_move(g) is not None:
            winning_move = self.winning_move(g)
            print(winning_move)
            func(winning_move)
            return winning_move
        elif self.blocking_move(g) is not None:
            blocking_move = self.blocking_move(g)
            print(blocking_move)
            func(blocking_move)
            return blocking_move
        else:
            basic_move = self.basic_move(g)
            print(basic_move)
            func(basic_move)
            return basic_move

    def winning_move(self, g):
        for move in range(self.choices):
            test_board = self.test_move(g, move)
            if g.check_winner_horizontal(test_board) or \
                    g.check_winner_vertical(test_board) or \
                    g.check_winner_diagonal(test_board):
                return move

    def blocking_move(self, g):
        for move in range(self.choices):
            test_board = self.test_move(g, move, True)
            if g.check_winner_horizontal(test_board) or \
                    g.check_winner_vertical(test_board) or \
                    g.check_winner_diagonal(test_board):
                if g.board[0][move] == g.BLANK:
                    return move

    def basic_move(self, g):
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
