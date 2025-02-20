import time
import matplotlib.pyplot as plt
import sys

def matrix_multiply(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]
    ]

def matrix_power(matrix, n):
    result = [[1, 0], [0, 1]] 
    base = matrix
    
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        n //= 2
    return result

def fibonacci(n):
    if n == 0:
        return 0
    matrix = [[0, 1], [1, 1]]
    result_matrix = matrix_power(matrix, n)
    return result_matrix[0][0]

if __name__ == "__main__":
    sys.set_int_max_str_digits(1000000)
    
    n_values = list(range(1, 500000, 10000))
    times = []

    # Measure execution time for different values of n
    for n in n_values:
        start = time.time()
        fibonacci(n)
        end = time.time()
        times.append(end - start)

    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, times, label="Matrix Power Method", color="b", marker="o")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("Time (seconds, logarithmic scale)")
    plt.title("Time Complexity of Fibonacci Matrix Power Method")
    plt.legend()
    plt.grid(True)
    plt.show()
