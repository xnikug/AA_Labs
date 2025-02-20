import timeit
import matplotlib.pyplot as plt

def fib_fast_doubling(n):
    def fib_dbl(m):
        if m == 0:
            return (0, 1)
        
        a, b = fib_dbl(m // 2)
        c = a * (2 * b - a)
        d = b * b + a * a
        
        if m % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)
    
    return fib_dbl(n)[0]
if __name__=='__main__':
    # Measure execution times
    n_values = list(range(0, 500001, 50000))
    time_values = []

    for n in n_values:
        time_taken = timeit.timeit(lambda: fib_fast_doubling(n), number=10) / 10
        time_values.append(time_taken)
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, time_values, marker='o', linestyle='-', color='b', label='Fast Doubling Fibonacci')
    plt.xlabel('n')
    plt.ylabel('Execution Time (s)')
    plt.title('Execution Time of Fast Doubling Fibonacci')
    plt.legend()
    plt.grid()
    plt.show()
