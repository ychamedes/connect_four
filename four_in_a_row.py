##############################################################################
# FILE : four_in_a_row.py
# WRITER : Jason Greenspan, jasonmg, 336126362; Yonatan Chamudot, ychamudot,
#  312516289
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION: Defines the GameBoard class that controls the GUI of
# # four in a row game. Implements other classes to run the game.
##############################################################################

import sys
import tkinter as tki
from communicator import Communicator
from game import Game
from ai import AI

ARGS_NUMBER_WO_IP = 3
ARGS_NUMBER_WITH_IP = 4
IS_HUMAN_ARG = 1
PORT_ARG = 2
IP_ARG = 3
INVALID_ARGUMENTS_MSG = "Illegal program arguments."
MIN_PORT = 1000
MAX_PORT = 65535
BOARD_COLUMNS = 7
BOARD_ROWS = 6
BUTTONS_ROW = 1
PLAYER_1 = 0
PLAYER_2 = 1
PLAYER_1_TITLE = "Connect Four - Red"
PLAYER_2_TITLE = "Connect Four - Yellow"
BG_COLOR = "blue"
BLANK_TILE_FILE = "blank_tile.gif"
PLAYER_1_PIECE_FILE = "red_piece.gif"
PLAYER_2_PIECE_FILE = "yellow_piece.gif"
P1_COLOR = "red"
P2_COLOR = "yellow"
MOUSE_OVER_COLOR = "white"
P1_WIN_MSG = "Red wins!"
P2_WIN_MSG = "Yellow wins!"
DRAW_MSG = "It's a draw!"


class GameBoard:
    def __init__(self, root, game, ai, communicator, is_human, server_status):
        self._root = root
        self._game = game
        self._ai = ai
        self._is_human = is_human
        self.__communicator = communicator
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)
        self.__build_board()
        if server_status:
            self._my_turn = True
            self._root.title(PLAYER_1_TITLE)
        else:
            self._my_turn = False
            self._root.title(PLAYER_2_TITLE)
        self.__ai_turn()


    def __build_board(self):
        """Builds GUI of board (row of buttons and empty tiles) when
        GameBoard is initialized."""

        self.__buttons = []
        self.__tiles = {}
        self.__background_tile_img = tki.PhotoImage(file=BLANK_TILE_FILE)

        for i in range(BOARD_ROWS + BUTTONS_ROW):
            for j in range(BOARD_COLUMNS):
                # Row of buttons to add piece in respective column.
                if i == 0:
                    button = tki.Button(self._root, height = 3, width = 10,
                                        command=self.__make_button(j))
                    button.config(bg=P1_COLOR) #Player 1 always goes first.
                    button.bind("<Enter>", self.__mouse_on(j))
                    button.bind("<Leave>", self.__mouse_off(j))
                    button.grid(row=i, column=j)
                    self.__buttons.append(button)
                # Add blank tiles on rest of board.
                else:
                    tile = tki.Label(root, image=self.__background_tile_img,
                                     bg=BG_COLOR, borderwidth=0)
                    tile.image = self.__background_tile_img
                    tile.grid(row=i, column=j)
                    self.__tiles[(i,j)] = tile

    def __ai_turn(self):
        """If AI player is activated, makes move."""

        if self._my_turn:
            if not self._is_human:
                self.__communicator.send_message(self._ai.find_legal_move(
                    self._game, self.__update_board))
                winner = self._game.get_winner()
                if winner is not None:
                    self.__end_game(winner)
                self.__next_move(False)

    def __make_button(self, column_coord):
        """Adds piece to board if it is the turn of the player who pressed
        the button. Communicates that the piece was added and checks
        for winner."""

        def add_piece():
            if self._my_turn:
                self.__update_board(column_coord)
                self.__communicator.send_message(column_coord)
                winner = self._game.get_winner()
                if winner is not None:
                    self.__end_game(winner)
                self.__next_move(False)

        return add_piece

    def __mouse_on(self, column_coord):
        """Changes color of button if current player focuses on it."""

        def change_icon(event):
            button = self.__buttons[column_coord]
            if self._my_turn:
                if self._game.current_player == PLAYER_1:
                    button.config(bg=MOUSE_OVER_COLOR)
                elif self._game.current_player == PLAYER_2:
                    button.config(bg=MOUSE_OVER_COLOR)

        return change_icon

    def __mouse_off(self, column_coord):
        """Changes color of button back to original color when
         player leaves focuses on it."""

        def change_icon(event):
            button = self.__buttons[column_coord]
            if self._my_turn:
                if self._game.current_player == PLAYER_1:
                    button.config(bg=P1_COLOR)
                elif self._game.current_player == PLAYER_2:
                    button.config(bg=P2_COLOR)

        return change_icon

    def __update_board(self, column_coord):
        """Updates using game the location of added piece for player's
        choice. Adds appropriate piece to position in GUI."""

        self.__player_1_piece_img = tki.PhotoImage(file=PLAYER_1_PIECE_FILE)
        self.__player_2_piece_img = tki.PhotoImage(file=PLAYER_2_PIECE_FILE)

        # Get coordinates of new move (if legal) and adjust to board with
        # buttons row.
        y_coord, x_coord = self._game.make_move(column_coord)
        y_coord += BUTTONS_ROW
        tile = self.__tiles[(y_coord, x_coord)]

        # Check which player added the piece and add respective piece.
        if self._game.current_player == PLAYER_1:
            tile.config(image=self.__player_1_piece_img)
            tile.image = self.__player_1_piece_img
        elif self._game.current_player == PLAYER_2:
            tile.config(image=self.__player_2_piece_img)
            tile.image = self.__player_2_piece_img

    def __next_move(self, is_turn):
        """Changes to next players turn and updates color of buttons
        accordingly."""

        self._game.switch_player()
        self._my_turn = is_turn
        if self._game.current_player == PLAYER_1:
            for button in self.__buttons:
                button.config(bg=P1_COLOR)
        elif self._game.current_player == PLAYER_2:
            for button in self.__buttons:
                button.config(bg=P2_COLOR)

    def __end_game(self, winner):
        """Check for winner and end game if there is one (or draw)."""

        if winner == self._game.DRAW:
            self.__end_message(DRAW_MSG)
        elif winner == PLAYER_1:
            self.__end_message(P1_WIN_MSG, P1_COLOR)
        elif winner == PLAYER_2:
            self.__end_message(P2_WIN_MSG, P2_COLOR)

    def __end_message(self, message, color="black"):
        """Display message at top of board in given color.
         Overwrites buttons place in top row."""

        self.__message_display = tki.Label(self._root, text = message,
                                           justify = "center",
                                           font = ("Comic Sans MS", 20),
                                           fg = color, bg=BG_COLOR)
        self.__message_display.grid(row = 0, columnspan = BOARD_COLUMNS,
                                    sticky = tki.W+tki.E+tki.N+tki.S)

    def __handle_message(self, message):
        """Handles message from communicator: updates board,
        checks for winner, and prepares next move."""

        message = int(message)
        self.__update_board(message)
        winner = self._game.get_winner()
        if winner is not None:
            self.__end_game(winner)
            return
        self.__next_move(True)
        self.__ai_turn()


def check_args(args):
    """Checks system arguments for correct amount, values of is_human arg,
    and valid value for port arg. Raises exception if there is an error."""

    if len(args) != ARGS_NUMBER_WO_IP and len(args) != ARGS_NUMBER_WITH_IP:
        raise Exception(INVALID_ARGUMENTS_MSG, len(args))
    elif args[IS_HUMAN_ARG] != "human" and args[IS_HUMAN_ARG] != "ai":
        raise Exception(INVALID_ARGUMENTS_MSG, args[IS_HUMAN_ARG])
    elif int(args[PORT_ARG]) < MIN_PORT or int(args[PORT_ARG]) > MAX_PORT:
        raise Exception(INVALID_ARGUMENTS_MSG, args[PORT_ARG])
    else:
        return True


if __name__ == "__main__":
    if check_args(sys.argv):
        game1 = Game()
        ai = AI()
        root = tki.Tk()

        port = int(sys.argv[PORT_ARG])
        if sys.argv[IS_HUMAN_ARG] == "human":
            is_human = True
        elif sys.argv[IS_HUMAN_ARG] == "ai":
            is_human = False

        if len(sys.argv) == ARGS_NUMBER_WO_IP: # no IP given: is server
            com = Communicator(root, port)
            gb = GameBoard(root, game1, ai, com, is_human, True)
        elif len(sys.argv) == ARGS_NUMBER_WITH_IP:
            ip = sys.argv[IP_ARG]
            com = Communicator(root, port, ip)
            gb = GameBoard(root, game1, ai, com, is_human, False)

        root.mainloop()


# Tasks:
# 	- GUI: Highlight winning move (not sure how to do this simply)
#
# 3. Documentation:
#     - README
# 	- Add comments
