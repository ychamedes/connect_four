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
BG_COLOR = "blue"
P1_WIN_MSG = "Red wins!"
P2_WIN_MSG = "Yellow wins!"
P1_COLOR = "red"
P2_COLOR = "yellow"
DRAW_MSG = "It's a draw!"


class GameBoard:
    def __init__(self, root, game, ai, communicator, server_status):
        self._root = root
        self._game = game
        self._ai = ai
        self._player1 = True
        self._player2 = True
        self.__communicator = communicator
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)
        self.__build_board()
        self._root.title("Connect Four")
        if server_status:
            self._my_turn = True
        else:
            self._my_turn = False
        self._ai_turn()


    def __build_board(self):

        self.__buttons = []

        for i in range(BOARD_ROWS + BUTTONS_ROW):
            for j in range(BOARD_COLUMNS):
                # Row of buttons to add piece in respective column.
                if i == 0:
                    button = tki.Button(self._root, height=3, width=10,
                                        command=self.__make_button(j))
                    if self._game.current_player == PLAYER_1:
                        button.config(bg=P1_COLOR)
                    button.grid(row=i, column=j)
                    self.__buttons.append(button)
                # Add blank tiles on rest of board.
                else:
                    tile = tki.Label(root, image=background_tile_img,
                                     bg=BG_COLOR, borderwidth=0)
                    tile.image = background_tile_img
                    tile.grid(row=i, column=j)

    def _ai_turn(self):
        # Check if AI player.
        if self._my_turn:
            if (self._game.current_player == self._game.PLAYER_ONE and not
                    self._player1) or (self._game.current_player ==
                                           self._game.PLAYER_TWO and not self._player2):
                self.__communicator.send_message(self._ai.find_legal_move(self._game, self.__update_board))
                winner = self._game.get_winner()
                if winner is not None:
                    self._end_game(winner)
                self.__next_move(False)

    def __make_button(self, column_coord):

        def __add_piece():
            if self._my_turn:
                self.__update_board(column_coord)
                self.__communicator.send_message(column_coord)
                winner = self._game.get_winner()
                if winner is not None:
                    self._end_game(winner)
                self.__next_move(False)


        return __add_piece

    def __update_board(self, column_coord):

        # Get coordinates of new move (if legal) and adjust to board with
        # buttons row.
        self.__y_coord, self.__x_coord = self._game.make_move(column_coord)
        self.__y_coord += BUTTONS_ROW

        # Check which player added the piece and add respective piece.
        if self._game.current_player == PLAYER_1:
            player_1_piece = tki.Label(root, image=player_1_piece_img,
                                       bg=BG_COLOR, borderwidth=0)
            player_1_piece.image = player_1_piece_img
            player_1_piece.grid(row=self.__y_coord,
                                column=self.__x_coord)
        elif self._game.current_player == PLAYER_2:
            player_2_piece = tki.Label(root, image=player_2_piece_img,
                                       bg=BG_COLOR, borderwidth=0)
            player_2_piece.image = player_2_piece_img
            player_2_piece.grid(row=self.__y_coord,
                                column=self.__x_coord)

    def __next_move(self, is_turn):

        self._game.switch_player()
        self._my_turn = is_turn
        if self._game.current_player == PLAYER_1:
            for button in self.__buttons:
                button.config(bg=P1_COLOR)
        elif self._game.current_player == PLAYER_2:
            for button in self.__buttons:
                button.config(bg=P2_COLOR)


    def _end_game(self, winner):
        # Check for winner and end game if there is one (or draw).
        if winner == self._game.DRAW:
            self._end_message(DRAW_MSG)
        elif winner == PLAYER_1:
            self._end_message(P1_WIN_MSG, P1_COLOR)
        elif winner == PLAYER_2:
            self._end_message(P2_WIN_MSG, P2_COLOR)
        # Disable any more pieces being added to the board.
        for button in self.__buttons:
            button.config(state="disabled")


    def _end_message(self, message, color="black"):
        self.__message_display = tki.Label(self._root, text= message,
                                           justify="center",
                                           font=("Comic Sans MS", 20),
                                           fg=color, bg=BG_COLOR)
        self.__message_display.grid(row=0, columnspan=BOARD_COLUMNS,
                                    sticky=tki.W+tki.E+tki.N+tki.S)

    def __handle_message(self, message):
        message = int(message)
        self.__update_board(message)
        winner = self._game.get_winner()
        if winner is not None:
            self._end_game(winner)
            return
        self.__next_move(True)
        self._ai_turn()


if __name__ == "__main__":
    game1 = Game()
    ai = AI()
    root = tki.Tk()
    port = 8000
    var = 1
    if var == 1:
        server = True
    else:
        server = False

    # Load icons of pieces.
    background_tile_img = tki.PhotoImage(file="blank_tile.gif")
    player_1_piece_img = tki.PhotoImage(file="red_piece.gif")
    player_2_piece_img = tki.PhotoImage(file="yellow_piece.gif")

    if server:
        com = Communicator(root, port)
        gb = GameBoard(root, game1, ai, com, True)
    else:
        ip = socket.gethostbyname(socket.gethostname())
        com = Communicator(root, port, ip)
        gb = GameBoard(root, game1, ai, com, False)

    root.mainloop()


# Tasks:
# 1. Debugging:
#   - Illegal move crashes game
#
# 2. Design:
# 	- Gameplay: Assign players (human or AI) from sys.argv
# 	- GUI: Scroll over with buttons
# 	- GUI: Highlight winning move (not sure how to do this simply)
#
# 3. Documentation:
# 	- Docstrings for all functions
# 	- Add comments
# 	- Get rid of unnecessary code (disabling buttons?)
# 	- Clean up Game class to proper OOP notation
