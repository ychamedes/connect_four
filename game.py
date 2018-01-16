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

    def __init__(self):
        # self.board = []
        # index = 0
        # for r in range(self.ROWS):
        #     row_list = []
        #     for c in range(self.COLUMNS):
        #         row_list.append(index)
        #         index += 1
        #     self.board.append(row_list)

        self.board = []
        for r in range(self.ROWS):
            row_list = []
            for c in range(self.COLUMNS):
                row_list.append(self.BLANK)
            self.board.append(row_list)

        self.current_player = self.PLAYER_ONE

    def make_move(self, column):
        print("make move")
        current_color = self.get_current_player()
        for row in range(self.ROWS):
            if self.board[row][column] != self.BLANK:
                if row == 0:
                    #pass
                    raise Exception("Illegal Move!")
                else:
                    self.board[row - 1][column] = current_color
            else:
                if row == self.ROWS - 1:
                    self.board[row][column] = current_color

    def get_winner(self):
        winner = None
        if self.check_winner_horizontal() or self.check_winner_diagonal() or\
                self.check_winner_vertical():
            print("winner")
            winner = self.current_player
        return winner

    def check_winner_horizontal(self):
        for row in self.board:
            streak = []
            if row[self.MIDDLE_OF_ROW] != self.BLANK:
                streak.append(self.MIDDLE_OF_ROW)
                # Compare first and last elements of streak with neighboring
                #  spaces in the row.
                while len(streak) < self.WIN_NUMBER:
                    if row[streak[0]] == row[streak[0] - 1]:
                        streak.insert(0, streak[0] - 1)
                    elif row[streak[-1]] == row[streak[-1] + 1]:
                        streak.append(streak[-1] + 1)
                    else:
                        break
                if len(streak) == self.WIN_NUMBER:
                    return True

    def check_winner_vertical(self):
        column_matrix = []
        for column in range(self.COLUMNS):
            column_list = []
            for row in self.board:
                column_list.append(row[column])
            column_matrix.append(column_list)
        for row in column_matrix:
            streak = []
            if row[self.MIDDLE_OF_COLUMN] != self.BLANK:
                streak.append(self.MIDDLE_OF_COLUMN)
                # Compare first and last elements of streak with neighboring
                #  spaces in the column.
                while len(streak) < self.WIN_NUMBER:
                    if row[streak[0]] == row[streak[0] - 1]:
                        streak.insert(0, streak[0]- 1)
                    elif row[streak[-1]] == row[streak[-1] + 1]:
                        streak.append(streak[-1] + 1)
                    else:
                        break
                if len(streak) == self.WIN_NUMBER:
                    return True

    def check_winner_diagonal(self):
        diagonal_list = self.get_diagonals()
        for diagonal in diagonal_list:
            streak = []
            if diagonal[len(diagonal) // 2] != self.BLANK:
                streak.append(len(diagonal) // 2)
                # Compare first and last elements of streak with neighboring
                #  spaces in the column.
                while len(streak) < self.WIN_NUMBER:
                    if diagonal[streak[0]] == diagonal[streak[0] - 1]:
                        streak.insert(0, streak[0]- 1)
                    elif diagonal[streak[-1]] == diagonal[streak[-1] + 1]:
                        streak.append(streak[-1] + 1)
                    else:
                        break
                if len(streak) == self.WIN_NUMBER:
                    return True



    def get_diagonals(self):
        reverse_board = []
        for row in self.board:
            reverse_board.append(row[::-1])
        diagonal_list = []
        for line in range(self.ROWS - 1):
            line_list_right = []
            line_list_left = []
            column = 0
            while line >= 0 and column <= self.COLUMNS:
                line_list_right.append(self.board[line][column])
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
                line_list_right.append(self.board[line][column])
                line_list_left.append(reverse_board[line][column])
                line -= 1
                column += 1
            if len(line_list_right) >= self.WIN_NUMBER:
                diagonal_list.append(line_list_right)
            if len(line_list_left) >= self.WIN_NUMBER:
                diagonal_list.append(line_list_left)
        return diagonal_list


    def get_player_at(self, row, col):
        pass

    def get_current_player(self):
        return self.current_player

    def switch_player(self):
        if self.current_player == self.PLAYER_ONE:
            self.current_player = self.PLAYER_TWO
            return
        if self.current_player == self.PLAYER_TWO:
            self.current_player = self.PLAYER_ONE
            return

    def __repr__(self):
        for row in self.board:
            print(row)

game1 = Game()
game1.__repr__()
while True:
    game1.make_move(int(input("column")))
    game1.__repr__()
    game1.get_winner()
    game1.switch_player()
