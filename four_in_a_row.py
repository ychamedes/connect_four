import tkinter as tki
import socket
from communicator import Communicator
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
    def __init__(self, root, game, ai, communicator):
        self._root = root
        self._game = game
        self._ai = ai
        self._communicator = communicator
        self._buttons = []
        self._player1 = True
        self._player2 = False
        self._root.title("Connect Four")
        communicator.bind_action_to_message(self._handle_message)

        for i in range(BOARD_ROWS + BUTTONS_ROW):
            for j in range(BOARD_COLUMNS):
                # Row of buttons to add piece in respective column.
                if i == 0:
                    self._button = tki.Button(self._root, text=j,
                                              height=1, width=10,
                                              command=self._make_button(j))
                    self._button.grid(row=i, column=j)
                    self._buttons.append(self._button)
                # Add blank tiles on rest of board.
                else:
                    tile = tki.Label(root, image=background_tile_img,
                                     bg="blue", borderwidth=0)
                    tile.image = background_tile_img
                    tile.grid(row=i, column=j)

            self.play_game()

    def _make_button(self, column_coord):

        def _add_piece():

            # Get coordinates of new move (if legal) and adjust to board with
            # buttons row.
            y_coord, x_coord = self._game.make_move(column_coord)
            y_coord += BUTTONS_ROW

            # Check which player added the piece and add respective piece.
            if self._game.current_player == PLAYER_1:
                player_1_piece = tki.Label(root, image=player_1_piece_img,
                                           bg="blue", borderwidth=0)
                player_1_piece.image = player_1_piece_img
                player_1_piece.grid(row=y_coord, column=x_coord)
            elif self._game.current_player == PLAYER_2:
                player_2_piece = tki.Label(root, image=player_2_piece_img,
                                           bg="blue", borderwidth=0)
                player_2_piece.image = player_2_piece_img
                player_2_piece.grid(row=y_coord, column=x_coord)


        return _add_piece

    def add_ai_piece(self, column_coord):
        # Get coordinates of new move (if legal) and adjust to board with
        # buttons row.
        y_coord, x_coord = self._game.make_move(column_coord)
        y_coord += BUTTONS_ROW

        # Check which player added the piece and add respective piece.
        if self._game.current_player == PLAYER_1:
            player_1_piece = tki.Label(root, image=player_1_piece_img,
                                       bg="blue", borderwidth=0)
            player_1_piece.image = player_1_piece_img
            player_1_piece.grid(row=y_coord, column=x_coord)
        elif self._game.current_player == PLAYER_2:
            player_2_piece = tki.Label(root, image=player_2_piece_img,
                                       bg="blue", borderwidth=0)
            player_2_piece.image = player_2_piece_img
            player_2_piece.grid(row=y_coord, column=x_coord)

    def play_game(self):
        self.makemove
        self._communicator.send_message(self._game)
        winner = self._game.get_winner()
        if winner is not None:
            self._end_game(winner)
        else:
            self.play_game()
        self._game.switch_player()

    def _end_game(self, winner):
        # Check for winner and end game if there is one (or draw).
        if winner == self._game.DRAW:
            self._end_message(DRAW_MSG)
        elif winner == PLAYER_1:
            self._end_message(P1_WIN_MSG)
        elif winner == PLAYER_2:
            self._end_message(P2_WIN_MSG)
        # Disable any more pieces being added to the board.
        for button in self._buttons:
            button.config(state="disabled")


    def _end_message(self, message):
        self._message_box = tki.Toplevel()
        message_display = tki.Entry(self._message_box, justify="center",
                                    width=50)
        message_display.pack()
        message_display.insert(0, message)

    def _handle_message(self, message):

        def _update_board():
            




if __name__ == "__main__":
    game1 = Game()
    ai = AI()
    root = tki.Tk()
    port = 8000
    com = Communicator(root, port, socket.gethostbyname(socket.gethostname()))
    server = False
    if server:
        com.connect()

    background_tile_img = tki.PhotoImage(file="blank_tile.gif")
    player_1_piece_img = tki.PhotoImage(file="red_piece.gif")
    player_2_piece_img = tki.PhotoImage(file="yellow_piece.gif")

    gb = GameBoard(root, game1, ai, com)

    root.mainloop()
