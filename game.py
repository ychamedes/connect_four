
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
        current_color = self.get_current_player()
        self.number_of_moves += 1
        if column not in range(self.COLUMNS):
            raise Exception("Illegal Move!")
        for row in range(self.ROWS):
            if self.board[row][column] != self.BLANK:
                if row == 0:
                    raise Exception("Illegal Move!")
                else:
                    self.board[row - 1][column] = current_color
                    return (row - 1, column)
                    break
            else:
                if row == self.ROWS - 1:
                    self.board[row][column] = current_color
                    return (row, column)
                else:
                    continue

    def get_winner(self):
        winner = None
        if self.check_winner_horizontal() or self.check_winner_diagonal() or \
                self.check_winner_vertical():
            print(self.check_winner_horizontal(),
                  self.check_winner_diagonal(), self.check_winner_vertical())
            print("winner")
            winner = self.current_player
        if self.number_of_moves == self.max_moves:
            print("draw")
            return Game.DRAW

        return winner

    def check_winner_horizontal(self, *args):
        board = self.board
        if args:
            board = list(args)[0]
        for row in board:
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
                        # print(row[streak[-1]] == row[streak[-1] + 1],
                        #       row[streak[-1]], row[streak[-1] + 1])
                    else:
                        break
                if len(streak) == self.WIN_NUMBER:
                    return True

    def check_winner_vertical(self, *args):
        board = self.board
        if args:
            board = list(args)[0]
        column_matrix = []
        for column in range(self.COLUMNS):
            column_list = []
            for row in board:
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
                        streak.insert(0, streak[0] - 1)
                    elif row[streak[-1]] == row[streak[-1] + 1]:
                        streak.append(streak[-1] + 1)
                    else:
                        break
                if len(streak) == self.WIN_NUMBER:
                    return True

    def check_winner_diagonal(self, *args):
        if args:
            diagonal_list = self.get_diagonals(list(args)[0])
        else:
            diagonal_list = self.get_diagonals()
        for diagonal in diagonal_list:
            streak = []
            if diagonal[len(diagonal) // 2] != self.BLANK:
                streak.append(len(diagonal) // 2)
                # Compare first and last elements of streak with neighboring
                #  spaces in the column.
                while len(streak) < self.WIN_NUMBER:
                    if diagonal[streak[0]] == diagonal[streak[0] - 1]:
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
        board = self.board
        if args:
            board = list(args)[0]
        reverse_board = []
        for row in board:
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
        result = self.board[row][col]
        if result == self.BLANK:
            return None
        else:
            return result

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
        print('-------------------------')
        print('   '.join(str(x) for x in range(self.COLUMNS)))
        for row in self.board:
            print('   '.join(str(row[x]) for x in range(self.COLUMNS)))
