from game import Game
import communicator
from ai import AI


game1 = Game()
ai = AI()
game1.__repr__()
player1 = True
player2 = False
while True:
    if player1 != player2:
        if not player1:
            ai_player = game1.PLAYER_ONE
        else:
            ai_player = game1.PLAYER_TWO
        if game1.get_current_player() == ai_player:
            ai.find_legal_move(game1, game1.make_move)
        else:
            game1.make_move(int(input("column")))
        game1.__repr__()
        game1.get_winner()
        game1.switch_player()
    else:
        if player1:
            game1.make_move(int(input("column")))
            game1.__repr__()
            game1.get_winner()
            game1.switch_player()
        else:
            ai.find_legal_move(game1, game1.make_move)
            game1.__repr__()
            game1.get_winner()
            game1.switch_player()
