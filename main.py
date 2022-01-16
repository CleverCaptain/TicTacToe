from enum import Enum, auto


class GameState(Enum):
    X_WINS = "X wins"
    O_WINS = "O wins"
    DRAW = "Draw"
    GAME_NOT_FINISHED = auto()
    IMPOSSIBLE = auto()


class Board:
    def __init__(self):
        self.cells = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.empty_cells = 9
        self.num_of_X = 0
        self.num_of_O = 0

    def same_row(self):
        return_value = "-"
        for row in self.cells:
            row_lower = [e.upper() for e in row]
            if ((row_lower[0] == 'X' or row_lower[0] == 'O')
                    and row_lower[0] == row_lower[1] == row_lower[2]):
                if return_value == "-":
                    return_value = row[0]
                else:
                    return "*"
        return return_value

    def same_col(self):
        return_value = "-"
        for i in range(3):
            col_upper = [self.cells[0][i].upper(), self.cells[1][i].upper(), self.cells[2][i].upper()]
            if ((col_upper[0] == 'X' or col_upper[0] == 'O')
                    and col_upper[0] == col_upper[1] == col_upper[2]):
                if return_value == "-":
                    return_value = self.cells[1][i]
                else:
                    return "*"
        return return_value

    def same_diagonal(self):
        diag_upper1 = [self.cells[0][0], self.cells[1][1], self.cells[2][2]]
        diag_upper1 = [e.upper() for e in diag_upper1]
        diag_upper2 = [self.cells[0][2], self.cells[1][1], self.cells[2][0]]
        diag_upper2 = [e.upper() for e in diag_upper2]
        if (((diag_upper1[0] == 'X' or diag_upper1[0] == 'O')
             and diag_upper1[0] == diag_upper1[1] == diag_upper1[2])
                or ((diag_upper2[0] == 'X' or diag_upper2[0] == 'O')
                    and diag_upper2[0] == diag_upper2[1] == diag_upper2[2])):
            return self.cells[1][1]
        return "-"

    def find_state(self):
        diff = self.num_of_X - self.num_of_O
        is_impossible = diff < -1 or diff > 1
        game_state = None
        if is_impossible:
            game_state = GameState.IMPOSSIBLE
            print("Impossible")
        else:
            same_row = self.same_row()
            same_col = self.same_col()
            same_diagonal = self.same_diagonal()
            if same_row == "*" or same_col == "*":
                game_state = GameState.IMPOSSIBLE
                print("Impossible")
            else:
                if same_row == same_col == same_diagonal == "-":
                    if self.empty_cells:
                        game_state = GameState.GAME_NOT_FINISHED
                    else:
                        game_state = GameState.DRAW
                else:
                    winner = None
                    if same_row != "-":
                        winner = same_row
                    elif same_col != "-":
                        winner = same_col
                    elif same_diagonal != "-":
                        winner = same_diagonal
                    else:
                        print("ERROR-Unable to find winner!")
                    if winner.upper() == 'X':
                        game_state = GameState.X_WINS
                    elif winner.upper() == 'O':
                        game_state = GameState.O_WINS
        return game_state

    def add_x(self, x, y):
        self.cells[x][y] = 'X'

    def add_o(self, x, y):
        self.cells[x][y] = 'O'

    def add_xo(self, coordinates, player):
        valid = False
        if len(coordinates) == 1:
            if coordinates[0].isdigit():
                print("Enter two numbers!")
            else:
                print("You should enter numbers!")
        elif len(coordinates) == 2:
            x = coordinates[0]
            y = coordinates[1]
            if x.isdigit() and y.isdigit():
                x = int(x)
                y = int(y)
                x -= 1
                y -= 1
                if 0 <= x < 3 and 0 <= y < 3:
                    if self.cells[x][y] == ' ':
                        valid = True
                        self.empty_cells -= 1
                        if player == 'X':
                            self.add_x(x, y)
                            self.num_of_X += 1
                        else:
                            self.add_o(x, y)
                            self.num_of_O += 1
                    else:
                        print("This cell is occupied! Choose another one!")
                else:
                    print("Coordinates should be from 1 to 3!")
            else:
                print("You should enter numbers!")
        else:
            print("You should enter only 2 numbers!")
        return valid

    def print_board(self):
        print("---------")
        for row in self.cells:
            print("|", row[0], row[1], row[2], "|")
        print("---------")


if __name__ == '__main__':
    board = Board()
    board.print_board()
    c = 'X'
    board_state = board.find_state()
    while board_state == GameState.GAME_NOT_FINISHED:
        valid_input = False
        while not valid_input:
            valid_input = board.add_xo(input("Enter the coordinates: ").split(), c)
        c = 'O' if c == 'X' else 'X'
        board.print_board()
        board_state = board.find_state()
    print(board_state.value)
