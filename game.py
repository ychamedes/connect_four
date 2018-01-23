##############################################################################
# FILE : game.py
# WRITER : Jason Greenspan, jasonmg, 336126362; Yonatan Chamudot, ychamudot,
#  312516289
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION: Defines the Game class, which sets the rules and gameplay of
# the connect four game
##############################################################################

class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    COLUMNS = 7
    ROWS = 6
    WIN_NUMBER = 4
    MIDDLE_OF_ROW = 3
    MIDDLE_OF_COLUMN = 2
    BLANK = "_"
    INITIAL_MOVES = 0

    def __init__(self):
        """Initializes a Game object"""
        self.board = []
        for r in range(Game.ROWS):
            row_list = []
            for c in range(Game.COLUMNS):
                row_list.append(Game.BLANK)
            self.board.append(row_list)

        self.current_player = Game.PLAYER_ONE
        self.number_of_moves = Game.INITIAL_MOVES
        self.max_moves = Game.ROWS * Game.COLUMNS

    def make_move(self, column):
        """Take an int representing a column on the game board, and add a
        piece representing the current player's color to the column """
        current_color = self.get_current_player()
        self.number_of_moves += 1
        if column not in range(self.COLUMNS):
            raise Exception("Illegal Move!")
        for row in range(self.ROWS):
            if self.board[row][column] != self.BLANK: #Checks if the column
                if row == 0:                          #is full
                    raise Exception("Illegal Move!")
                else:
                    self.board[row - 1][column] = current_color
                    return (row - 1, column)
            else:
                if row == self.ROWS - 1:
                    self.board[row][column] = current_color
                    return (row, column)
                else:
                    continue

    def get_winner(self):
        """Check if the current game board contains four pieces of the same
        color in a row horizontally, vertically, or diagonally. Also checks
        if the game has ended in a draw. If there is a winner, return which
        player won, and if there is a draw return the DRAW constant"""
        winner = None
        if self.check_winner_horizontal() or self.check_winner_diagonal() or \
                self.check_winner_vertical():
            winner = self.current_player
        if self.number_of_moves == self.max_moves:
            return Game.DRAW
        return winner

    def check_winner_horizontal(self, *args):
        """Checks if there is a winner horizontally. If there is, return True"""
        board = self.board
        if args:    #This allows the method to be used by the ai class
            board = list(args)[0]
        for row in board:
            streak = []
            if row[self.MIDDLE_OF_ROW] != self.BLANK: #If the middle space
                # in a row is blank, there can be no winner in that row
                streak.append(self.MIDDLE_OF_ROW)
                # Compare first and last elements of streak with neighboring
                #  spaces in the row.
                while len(streak) < self.WIN_NUMBER:
                    if row[streak[0]] == row[streak[0] - 1] and streak[0] - \
                            1 >= 0:
                        streak.insert(0, streak[0] - 1)
                    elif row[streak[-1]] == row[streak[-1] + 1] and streak[
                        -1] + 1 < len(row):
                        streak.append(streak[-1] + 1)
                    else:
                        break
                    if len(streak) == self.WIN_NUMBER:
                        return True

    def check_winner_vertical(self, *args):
        """Check if there is a winner vertically. If there is, return True"""
        board = self.board
        if args:   #This allows the method to be used by the ai class
            board = list(args)[0]
        column_matrix = []
        for column in range(self.COLUMNS):  #Creates a new game board with
                                            # flipped axes
            column_list = []
            for row in board:
                column_list.append(row[column])
            column_matrix.append(column_list)
        for row in column_matrix:
            streak = []
            if row[self.MIDDLE_OF_COLUMN] != self.BLANK: #If the middle
                # space in a column is blank there can be no winner in that
                # column
                streak.append(self.MIDDLE_OF_COLUMN)
                # Compare first and last elements of streak with neighboring
                #  spaces in the column.
                while len(streak) < self.WIN_NUMBER:
                    if row[streak[0]] == row[streak[0] - 1] and streak[0] - \
                            1 >= 0:
                        streak.insert(0, streak[0] - 1)
                    elif row[streak[-1]] == row[streak[-1] + 1] and streak[
                        -1] + 1 < len(row):
                        streak.append(streak[-1] + 1)
                    else:
                        break
                if len(streak) == self.WIN_NUMBER:
                    return True

    def check_winner_diagonal(self, *args):
        """Checks if there is a winner diagonally. If there is, return True"""
        if args:   #This allows the method to be used by the ai class
            diagonal_list = self.get_diagonals(list(args)[0])
        else:  #Creates a list of all the diagonals with at least length 4
            diagonal_list = self.get_diagonals()
        for diagonal in diagonal_list:
            streak = []
            if diagonal[len(diagonal) // 2] != self.BLANK: #If the middle
                # space in the diagonal is blank there can be no winner in
                # that diagonal
                streak.append(len(diagonal) // 2)
                # Compare first and last elements of streak with neighboring
                #  spaces in the column.
                while len(streak) < self.WIN_NUMBER:
                    if diagonal[streak[0]] == diagonal[streak[0] - 1] and \
                            streak[0] - 1 >= 0:
                        streak.insert(0, streak[0] - 1)
                    elif streak[-1] + 1 < len(diagonal):
                        if diagonal[streak[-1]] == diagonal[streak[-1] + 1]:
                            streak.append(streak[-1] + 1)
                        else:
                            break
                    else:
                        break
                if len(streak) == self.WIN_NUMBER:
                    return True

    def get_diagonals(self, *args):
        """Return a list of all the diagonal rows in a game board. Filters
        the list so that it includes only diagonals of length 4 or greater"""
        board = self.board
        if args:  #This allows the method to be used by the ai class
            board = list(args)[0]
        reverse_board = []
        for row in board:  #Creates a board rotated the opposite direction
            reverse_board.append(row[::-1])
        diagonal_list = []
        for line in range(self.ROWS - 1):
            line_list_right = []
            line_list_left = []
            column = 0
            while line >= 0 and column <= self.COLUMNS:
                line_list_right.append(board[line][column])
                line_list_left.append(reverse_board[line][column])
                line -= 1
                column += 1
            if len(line_list_right) >= self.WIN_NUMBER:
                diagonal_list.append(line_list_right)
            if len(line_list_left) >= self.WIN_NUMBER:
                diagonal_list.append(line_list_left)
        for column in range(self.COLUMNS):
            line = self.ROWS - 1
            line_list_right = []
            line_list_left = []
            while column < self.COLUMNS:
                line_list_right.append(board[line][column])
                line_list_left.append(reverse_board[line][column])
                line -= 1
                column += 1
            if len(line_list_right) >= self.WIN_NUMBER:
                diagonal_list.append(line_list_right)
            if len(line_list_left) >= self.WIN_NUMBER:
                diagonal_list.append(line_list_left)
        return diagonal_list

    def get_player_at(self, row, col):
        """Take row and column coordinates and return the player whose piece
        is present at that location on the game board"""
        result = self.board[row][col]
        if result == self.BLANK:
            return None
        else:
            return result

    def get_current_player(self):
        """Return the current player"""
        return self.current_player

    def switch_player(self):
        """Switch the current player"""
        if self.current_player == self.PLAYER_ONE:
            self.current_player = self.PLAYER_TWO
            return
        if self.current_player == self.PLAYER_TWO:
            self.current_player = self.PLAYER_ONE
            return
