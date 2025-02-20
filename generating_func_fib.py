import sympy as sp
import time
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = sp.symbols('x')
    f = x / (1 - x - x**2)  #The Generating Function

    # Define expansion point on Origin
    x0 = 0

    n_values = range(1, 20)
    times = []
    print('The Fibanocci Terms:')
    for n in n_values:
        start_time = time.time() 
        # Compute the n-th Maclaurin coefficient
        coefficient = f.diff(x, n).subs(x, x0) / sp.factorial(n)
        print(f'{n}) {coefficient}')
        end_time = time.time()
        times.append(end_time - start_time)

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, times, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Taylor Coefficients (n)')
    plt.ylabel('Computation Time (seconds)')
    plt.title('Computation Time vs. Number of Taylor Coefficients')
    plt.grid(True)
    plt.show()
