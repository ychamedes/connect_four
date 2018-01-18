import tkinter as tki
import communicator
from game import Game
from ai import AI

COLUMNS = 7
ROWS = 6
PLAYER_1 = 0
PLAYER_2 = 1

class GameBoard:
    def __init__(self, root, game):
        self._root = root
        self._game = game
        
        for i in range(ROWS):
            for j in range(COLUMNS):
                # Row of buttons to add piece in respective column.
                if i == 0:
                    self._add_button = tki.Button(self._root, height = 1,
                                                  width = 12,
                                            command = self._make_button(j))
                    self._add_button.grid(row = i, column = j)
                # Add blank tiles on rest of board.
                else:
                    tile = tki.Label(root, image = background_tile_img,
                                     bg="blue", borderwidth = 0)
                    tile.image = background_tile_img
                    tile.grid(row = i, column = j)
    
    def _make_button(self, column_coord):
        def _add_piece():
            x_coord, y_coord = self._game.make_move(column_coord)
            self._game.switch_player()
            self._game.get_winner()
            # Check which player added the piece and add respective piece.
            if self._game.current_player == PLAYER_1:
                player_1_piece = tki.Label(root, image = player_1_piece_img,
                                           bg="blue", borderwidth = 0))
                player_1_piece.image = player_1_piece_img
                player_1_piece.grid(row = x_coord, column = y_coord)
            elif self._game.current_player == PLAYER_2:
                player_2_piece = tki.Label(root, image = player_2_piece_img,
                                           bg="blue", borderwidth = 0))
                player_2_piece.image = player_2_piece_img
                player_2_piece.grid(row = x_coord, column = y_coord)
        
        return _add_piece
        
    def end_msg(self):
        pass
    
if __name__ == "__main__":
    game1 = Game()
    ai = AI()
    root = tki.Tk()
    
    background_tile_img = tki.PhotoImage(file = "blank_tile.gif")
    player_1_piece_img = tki.PhotoImage(file = "red_piece.gif")
    player_2_piece_img = tki.PhotoImage(file = "yellow_piece.gif")
    
    GameBoard(root, game1)
    root.mainloop()
   

#while True:
#    if player1 != player2:
#        if not player1:
#            ai_player = game1.PLAYER_ONE
#        else:
#            ai_player = game1.PLAYER_TWO
#        if game1.get_current_player() == ai_player:
#            ai.find_legal_move(game1, game1.make_move)
#        else:
#            game1.make_move(int(input("column")))
#        game1.__repr__()
#        game1.get_winner()
#        game1.switch_player()
#    else:
#        if player1:
#            game1.make_move(int(input("column")))
#            game1.__repr__()
#            game1.get_winner()
#            game1.switch_player()
#        else:
#            ai.find_legal_move(game1, game1.make_move)
#            game1.__repr__()
#            game1.get_winner()
#            game1.switch_player()
