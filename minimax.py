from random import randint

def print_board(board):
    print("\n".join(map(str, board)))

def new_game(dim=8):
    """Generate a blank board.
    Input:
        dim : the number of squares in one row or column
    
    Output: a dim*dim list of 0s
    """
    return [[0 for i in range(dim)] for j in range(dim)]

def random_move(board, player):
    """Make a random move and return the new board"""
    dim = len(board)
    while True:
        try:
            return insert_stone(board, player, randint(0, dim), randint(0, dim))
        except:
            pass

def insert_stone(board, player, x, y):
    """Return a copy of the board with a new stone in (x, y).
    Input:
        board : the game state as an n*n list (n likely == 8)
        player : which player's is placing the stone (white == 1, black == -1)
        x : the index in the row to place the stone
        y : the index of the row to place the stone

    Output: a copy of the board with the new stone
    """
    if board[y][x] != 0:
        raise Exception("Trying to place stone where one has already been placed")
    board = list(map(lambda x: x.copy(), board))
    board[y][x] = player
    return board

def children(position, player):
    """Iterate over the possible moves from a given state.
    Input:
        position : the game state as an n*n list (n likely == 8)
        player : which player's move it is (white == 1, black == -1)
    
    Output: yields each possible move
    """
    dim = len(position)
    for x in range(dim): # index in the row
        for y in range(dim): # index of the row
            if position[y][x] == 0: # check if the move is valid
                yield insert_stone(position, player, x, y)

def evaluate_row(row):
    """Evaluate a given row for various threats
    Input:
        row : list of row
    Output: white and black threats [n, n, n, n], [n, n, n, n]
    """
    white_threats = [0, 0, 0, 0, 0, 0] # [win, straight threat, four threat, three threat, broken three, open two]
    black_threats = [0, 0, 0, 0, 0, 0]
    length = len(row)

    # look for a win
    for n in range(length-4):
        s = sum(row[n:n+5])
        if s == 5:
            return [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]
        elif s == -5:
            return [0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0]

    # look for straight threats (four in a row eg. [0, 1, 1, 1, 1, 0, 0, 0])
    for n in range(length-3):
        s = sum(row[n:n+4]) # check if all four squares have the same stone
        if s == 4:
            closed_sides = sum([row[n-1] == -1 if n-1 >= 0 else 0, row[n+4] == -1 if n+4<length else 0, n == 0, n == length-5])
            if closed_sides == 0:
                white_threats[1] += 1
            elif closed_sides == 1:
                white_threats[2] += 1
        elif s == -4:
            closed_sides = sum([row[n-1] == 1 if n-1 >= 0 else 0, row[n+4] == 1 if n+4<length else 0, n == 0, n == length-5])
            if closed_sides == 0:
                black_threats[1] += 1
            elif closed_sides == 1:
                black_threats[2] += 1

    # look for three threats (6 squares with 3 of the four center occupied eg. [0, 0, 1, 1, 1, 0, 0, 0])
    for n in range(1, length-4):
        s = sum(row[n:n+4])
        if s == 3 and -1 not in row[n:n+4] and row[n-1]+row[n+4] == 0:
            if row[n+1:n+3] == [1, 1]: # check if the three is broken
                white_threats[3] += 1
            else:
                white_threats[4] += 1
        if s == -3 and 1 not in row[n:n+4] and row[n-1]+row[n+4] == 0:
            if row[n+1:n+3] == [-1, -1]:
                black_threats[3] += 1
            else:
                black_threats[4] += 1

    # look for lines of two
    for n in range(length-1):
        s = sum(row[n:n+2])
        outer = sum(row[n-1:n+3])
        if s == 2 and outer == 2:
            white_threats[5] += 1
        if s == -2 and outer == -2:
            black_threats[5] += 1

    return white_threats, black_threats

def static_eval(position, player):
    """Return a static evaluation of the board. High values favor white low favor black.
    Input:
        position : the game state as an n*n list (n likely == 8)
        player : which player's move it is
    Output: how good the game is for white
    """
    weights = [100, 7, 3, 2, 1]

    dim = len(position)
    white_threats = [0, 0, 0, 0] # [straight threat, four threat, three threat, broken three]
    black_threats = [0, 0, 0, 0]

    # find the rows on the board
    horizontals = position
    verticals = [[position[x][y] for x in range(dim)] for y in range(dim)]
    downwards = [[position[y+x][x] for x in range(dim-y)] for y in range(dim)]
    downwards += [[position[y][x+y] for y in range(dim-x)] for x in range(1, dim)]
    upwards = [[position[y-x][x] for x in range(y+1)] for y in range(dim)]
    upwards += [[position[dim-y-1][x+y] for y in range(dim-x)] for x in range(1, dim)]

    rows = horizontals+verticals+downwards+upwards

    white_threats = [0, 0, 0, 0, 0]
    black_threats = [0, 0, 0, 0, 0]
    for row in rows:
        if 1 in row or -1 in row:
            white, black = evaluate_row(row)
            if white[0] > 0: # if a player has won in the poistion stop checking
                return float("inf")
            elif black[0] > 0:
                return float("-inf")
            else:
                # update the tallies
                white_threats[0] += white[1]
                white_threats[1] += white[2]
                white_threats[2] += white[3]
                white_threats[3] += white[4]
                white_threats[4] += white[5]

                black_threats[0] += black[1]
                black_threats[1] += black[2]
                black_threats[2] += black[3]
                black_threats[3] += black[4]
                black_threats[4] += black[5]

    if player == 1 and white_threats[0] > 0: # if the player can force a win return a very high value
        return 1000000*white_threats[0]      # if float("inf") was returned the ai would not be able to find the winning move so a very high but finite number is returned
    if player == -1 and black_threats[0] > 0:
        return 1000000*black_threats[0]

    return sum(w*t for w, t in zip(weights, white_threats))-sum(w*t for w, t in zip(weights, black_threats))



def minimax(position, player=1, depth=5, alpha=float("inf"), beta=float("-inf")):
    # if the depth is reached or the game is over
    if depth == 0:
        return static_eval(position, player)

    if player == 1:
        max_eval = float("-inf")
        for child in children(position, player):
            child_eval = minimax(child, -1, depth-1, alpha, beta)
            max_eval = max(max_eval, child_eval)
            alpha = max(alpha, child_eval)
            if beta <= alpha:
                break
        return max_eval

    elif player == -1:
        min_eval = float("inf")
        for child in children(position, player):
            child_eval = minimax(child, 1, depth-1, alpha, beta)
            min_eval = min(min_eval, child_eval)
            beta = min(beta, child_eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, player, depth=5):
    """Find the move that has the highest expected payoff"""
    if player == 1:
        return max(children(board, 1), key=lambda b: minimax(board, -1, depth))
    elif player == -1:
        return min(children(board, -1), key=lambda b: minimax(board, 1, depth))

if __name__ == '__main__':
    b = new_game()
    for i in range(10):
        b = random_move(b, 1-2*(i%2))
    print_board(b)
    print()
    for i in range(10):
        b = best_move(b, 1-2*(i%2))
        print_board(b)
        print(minimax(b, 1-2*(i%2)))