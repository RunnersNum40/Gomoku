from minimax import *

b = new_game(5)
for i in range(25):
    b = best_move(b, 1-2*(i%2), 3)
    print_big(b)
    print()