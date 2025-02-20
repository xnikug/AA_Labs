import time
import matplotlib.pyplot as plt

# Recursive Fibonacci function
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def measure_time(n_values):
    times = []
    for n in n_values:
        start = time.time()
        fibonacci(n)
        end = time.time()
        times.append(end - start)
    return times

if __name__ == '__main__':
    n_values = list(range(1, 40))
    times = measure_time(n_values)

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, times, marker='o', linestyle='-', color='b', label='Execution Time')
    plt.xlabel('n')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity of Recursive Fibonacci')
    plt.legend()
    plt.grid()
    plt.show()