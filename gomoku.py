"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    for row in board:
        for square in row:
            if square != " ":
                return False
    return True

def get_opposite(col):
    return "w" if col == "b" else "b"

def is_in_range(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board[y])

def is_seq(board, y, x, col):
    return is_in_range(board, y, x) and board[y][x] == col

def is_bound(board, y, x, col):
    return not (is_seq(board, y, x, col) or is_seq(board, y, x, " "))

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    col = board[y_end][x_end]
    end_blocked = is_bound(board, y_end+d_y, x_end+d_x, col)
    start_blocked = is_bound(board, y_end-(length*d_y), x_end-(length*d_x), col)

    if start_blocked and end_blocked:
        return "CLOSED"
    elif not start_blocked and not end_blocked:
        return "OPEN"
    return "SEMIOPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    y, x = y_start, x_start
    cur_len = 1 if is_seq(board, y, x, col) else 0
    while is_in_range(board, y, x):
        if not is_seq(board, y+d_y, x+d_x, col):
            if cur_len == length:
                result = is_bounded(board, y, x, length, d_y, d_x)
                #print("\t", result, y, x, length, d_y, d_x)
                open_seq_count += 1 if result == "OPEN" else 0
                semi_open_seq_count += 1 if result == "SEMIOPEN" else 0
            cur_len = 0
        else:
            cur_len += 1

        y += d_y
        x += d_x

    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    y_size = len(board)
    x_size = len(board[0])
    to_check = [[[0], range(x_size), 1, 0],  # vertical
                [range(y_size), [0], 0, 1],  # horizontal
                [[0], range(x_size), 1, 1],
                [range(1, y_size), [0], 1, 1],
                [[0], range(x_size), 1, -1],
                [range(1, y_size), [x_size-1], 1, -1]]

    for ys, xs, d_y, d_x in to_check:
        for y in ys:
            for x in xs:
                opens, semi_opens = detect_row(board, col, y, x, length, d_y, d_x)
                open_seq_count += opens
                semi_open_seq_count += semi_opens
    return open_seq_count, semi_open_seq_count


def search_max(board):
    move_y, move_x, max_score = 0, 0, -100000000000000000000000000000000
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b"
                move_score = score(board)
                if move_score > max_score:
                    move_y, move_x, max_score = y, x, move_score
                board[y][x] = " "

    return move_y, move_x

MAX_SCORE = 10000000

def score(board):

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    win_len = 5
    draw = True
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                draw = False
            for d_y, d_x in ((1, 0), (0, 1), (1, 1), (1, -1)):
                for col in ("w", "b"):
                    if not is_seq(board, y-d_y, x-d_x, col) and all(is_seq(board, y+i*d_y, x+i*d_x, col) for i in range(win_len)) and not is_seq(board, y+(win_len*d_y), x+(win_len*d_x), col):
                        return "White won" if col == "w" else "Black won"
    return "Draw" if draw else "Continue playing"


def print_board(board):
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        #print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            #print("Open rows of length %d: %d" % (i, open))
            #print("Semi-open rows of length %d: %d" % (i, semi_open))




def place_random(board, col):
    import random
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    while(board[y][x] != ' '):
        x = random.randint(0, 7)
        y = random.randint(0, 7)
    board[y][x] = col


def play_gomoku(board_size):
    import mcts
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    place_random(board, "b")
    place_random(board, "w")
    place_random(board, "b")
    place_random(board, "w")

    while True:
        #print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        #print("Computer move: (%d, %d)" % (move_y, move_x))
        #print(ai.move(board, "b"))
        board[move_y][move_x] = "b"
        print_board(board)
        #analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        #import cProfile
        #cProfile.runctx('mcts.move(board, "w")', globals(), locals())
        #print("Your move:")
        move_y, move_x = mcts.move(board, "w")
        #print(move_y, move_x)
        #move_y = int(input("y coord: "))
        #move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        #analysis(board)
        print_board(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    print(play_gomoku(8))
