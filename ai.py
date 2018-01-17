from game import Game
import random

class AI:

    def find_legal_move(self, g, func, timeout=None):
        move = random.choice(range(7))
        if g.board[0][move] == g.BLANK:
            func(move)
        else:
            if g.number_of_moves == g.max_moves:
                raise Exception("DRAW")
            self.find_legal_move(g, func)
