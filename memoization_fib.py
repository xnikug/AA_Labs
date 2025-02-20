import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(None)
def fib_memoization(n):
    if n < 2:
        return n
    return fib_memoization(n - 1) + fib_memoization(n - 2)
if __name__ == '__main__':
    # Measure execution times
    n_values = list(range(0, 501, 50))
    time_values = []

    for n in n_values:
        time_taken = timeit.timeit(lambda: fib_memoization(n), number=10) / 10
        time_values.append(time_taken)

    # Plot execution time
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, time_values, marker='o', linestyle='-', color='r', label='Memoization Fibonacci')
    plt.xlabel('n')
    plt.ylabel('Execution Time (s)')
    plt.title('Execution Time of Memoization Fibonacci')
    plt.legend()
    plt.grid()
    plt.show()
