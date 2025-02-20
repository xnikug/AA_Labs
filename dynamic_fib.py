import time
import matplotlib.pyplot as plt
import pandas as pd

# Dynamic Programming Fibonacci function
def fibonacci_dp(n):
    A = [0] * (n + 1)
    A[0], A[1] = 0, 1
    for i in range(2, n + 1):
        A[i] = A[i - 1] + A[i - 2]
    return A[n]

def measure_time_dp(n_values):
    times = []
    for n in n_values:
        start = time.time()
        fibonacci_dp(n)
        end = time.time()
        times.append(end - start)
    return times
if __name__ == '__main__':
    n_values = list(range(1, 10000, 499))
    times_dp = measure_time_dp(n_values)

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, times_dp, marker='s', linestyle='-', color='g', label='Dynamic Programming')
    plt.xlabel('n')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity of Dynamic Programming Fibonacci')
    plt.legend()
    plt.grid()
    plt.show()

    data = {str(n): [t] for n, t in zip(n_values, times_dp)}
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
