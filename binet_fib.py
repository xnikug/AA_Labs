from decimal import ROUND_HALF_EVEN, Context, Decimal
import sys
import time
import matplotlib.pyplot as plt
import pandas as pd

import matrix_fib

# Binet Formula Method for calculating Fibonacci numbers
def fibonacci_binet(n):
    cx = Context(prec=100, rounding=ROUND_HALF_EVEN)
    phi1 = Decimal((1 + Decimal(5**(1/2))))
    phi2 = Decimal((1 - Decimal(5**(1/2))))
    return round((cx.power(phi1, Decimal(n)) - cx.power(phi2, Decimal(n)))/(2**n* Decimal(5**(1/2))))

if __name__ == "__main__":
    sys.set_int_max_str_digits(100000)
    n_values = list(range(1, 100, 15))
    times = []
    nth_terms = []
    for n in n_values:
        start = time.time()
        fib_n = fibonacci_binet(n)
        real_fib_n = matrix_fib.fibonacci(n+1)
        print(f'Rank {n} Fibonacci term: {fib_n}. The real value: {real_fib_n}')
        end = time.time()
        execution_time = end - start
        times.append(execution_time)
        nth_terms.append(fib_n)


    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, times, label="Binet Formula", color="r", marker="x")
    plt.xlabel("n")
    plt.ylabel("Time (seconds)")
    plt.title("Time Complexity of Fibonacci Binet Formula Method")
    plt.legend()
    plt.grid(True)
    plt.show()
