from time import perf_counter_ns
from minimax import *
import matplotlib.pyplot as plt
from timeit import timeit


times = []
for d in range(200):
    times.append(timeit(f"best_move(new_game(), 1, {d})", globals=globals(), number=100)/100)

plt.scatter(range(200), times)
plt.show()



# for i in range(10):
#     b = random_move(b, 1-2*(i%2))
# print_board(b)
# print()
# for i in range(10):
#     b = max(children(b, 1-2*((i+1)%2)), key=lambda b: (1-2*(i%2))*minimax(b, 1-2*(i%2)))
#     print_board(b)
#     print(minimax(b, 1-2*(i%2)))