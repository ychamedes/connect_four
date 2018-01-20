import tkinter as tki
import communicator
from game import Game
from ai import AI

BOARD_COLUMNS = 7
BOARD_ROWS = 6
BUTTONS_ROW = 1
PLAYER_1 = 0
PLAYER_2 = 1
P1_WIN_MSG = "Red wins!"
P2_WIN_MSG = "Yellow wins!"
DRAW_MSG = "It's a draw!"

class GameBoard:
    def __init__(self, root, game):
        self._root = root
        self._game = game
        self._buttons = []
        
        for i in range(BOARD_ROWS + BUTTONS_ROW):
            for j in range(BOARD_COLUMNS):
                # Row of buttons to add piece in respective column.
                if i == 0:
                    self._button = tki.Button(self._root, text = j,
                                                  height = 1, width = 10,
                                            command = self._make_button(j))
                    self._button.grid(row = i, column = j)
                    self._buttons.append(self._button)
                # Add blank tiles on rest of board.
                else:
                    tile = tki.Label(root, image = background_tile_img,
                                     bg="blue", borderwidth = 0)
                    tile.image = background_tile_img
                    tile.grid(row = i, column = j)
    
    def _make_button(self, column_coord):
        
        def _add_piece():
            
            # Get coordinates of new move (if legal) and adjust to board with
            # buttons row.
            y_coord, x_coord = self._game.make_move(column_coord)
            y_coord += BUTTONS_ROW
            
            # Check which player added the piece and add respective piece.
            if self._game.current_player == PLAYER_1:
                player_1_piece = tki.Label(root, image = player_1_piece_img,
                                           bg="blue", borderwidth = 0)
                player_1_piece.image = player_1_piece_img
                player_1_piece.grid(row = y_coord, column = x_coord)
            elif self._game.current_player == PLAYER_2:
                player_2_piece = tki.Label(root, image = player_2_piece_img,
                                           bg="blue", borderwidth = 0)
                player_2_piece.image = player_2_piece_img
                player_2_piece.grid(row = y_coord, column = x_coord)
                
            # Check for winner and end game if there is one (or draw).
            winner = self._game.get_winner()
            if winner is not None:
                if winner == self._game.DRAW:
                    self._end_message(DRAW_MSG)
                elif winner == PLAYER_1:
                    self._end_message(P1_WIN_MSG)
                elif winner == PLAYER_2:
                    self._end_message(P2_WIN_MSG)         
            self._game.switch_player()
            
        return _add_piece
        
    def _end_message(self, message):
        self._message_box = tki.Toplevel()
        message_display = tki.Entry(self._message_box, justify="center",
                                    width=50)
        message_display.pack()
        message_display.insert(0, message)
        # Disable any more pieces being added to the board.
        for button in self._buttons:
            button.config(state="disabled")

if __name__ == "__main__":
    game1 = Game()
    ai = AI()
    root = tki.Tk()
    
    coin_img = tki.PhotoImage(file = "coin_img.gif")
    background_tile_img = tki.PhotoImage(file = "blank_tile.gif")
    player_1_piece_img = tki.PhotoImage(file = "red_piece.gif")
    player_2_piece_img = tki.PhotoImage(file = "yellow_piece.gif")

    GameBoard(root, game1)
    root.mainloop()
    
#player1 = False
#player2 = False
#while True:
#    if player1 != player2:
#        if not player1:
#            ai_player = game1.PLAYER_ONE
#        if not player2:
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
