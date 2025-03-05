import random
import time
import matplotlib.pyplot as plt

# Regular Bubble Sort
def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Improved Bubble Sort
def improved_bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Cocktail Shaker Sort (Bidirectional Bubble Sort)
def cocktail_shaker_sort(arr):
    arr = arr.copy()
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start += 1
    return arr

# Function to time the sorting process
def time_sorting_function(sort_func, arr):
    start_time = time.time()
    sort_func(arr)
    return time.time() - start_time

# Main function to compare and plot results
def compare_and_plot():
    sizes = [10, 50, 100, 200, 300, 400, 500]
    
    regular_times_worst = []
    improved_times_worst = []
    cocktail_times_worst = []
    
    regular_times_avg = []
    improved_times_avg = []
    cocktail_times_avg = []
    
    regular_times_best = []
    improved_times_best = []
    cocktail_times_best = []
    
    for size in sizes:
        arr_for_regular_worst = list(range(size, 0, -1))
        arr_for_improved_worst = arr_for_regular_worst.copy()
        arr_for_cocktail_worst = arr_for_regular_worst.copy()
        
        arr_for_regular_avg = [random.randint(1, size * 10) for _ in range(size)]
        arr_for_improved_avg = arr_for_regular_avg.copy()
        arr_for_cocktail_avg = arr_for_regular_avg.copy()
        
        arr_for_regular_best = list(range(size))
        arr_for_improved_best = arr_for_regular_best.copy()
        arr_for_cocktail_best = arr_for_regular_best.copy()

        regular_time_worst = time_sorting_function(bubble_sort, arr_for_regular_worst)
        regular_times_worst.append(regular_time_worst)

        improved_time_worst = time_sorting_function(improved_bubble_sort, arr_for_improved_worst)
        improved_times_worst.append(improved_time_worst)

        cocktail_time_worst = time_sorting_function(cocktail_shaker_sort, arr_for_cocktail_worst)
        cocktail_times_worst.append(cocktail_time_worst)

        regular_time_avg = time_sorting_function(bubble_sort, arr_for_regular_avg)
        regular_times_avg.append(regular_time_avg)

        improved_time_avg = time_sorting_function(improved_bubble_sort, arr_for_improved_avg)
        improved_times_avg.append(improved_time_avg)

        cocktail_time_avg = time_sorting_function(cocktail_shaker_sort, arr_for_cocktail_avg)
        cocktail_times_avg.append(cocktail_time_avg)

        regular_time_best = time_sorting_function(bubble_sort, arr_for_regular_best)
        regular_times_best.append(regular_time_best)

        improved_time_best = time_sorting_function(improved_bubble_sort, arr_for_improved_best)
        improved_times_best.append(improved_time_best)

        cocktail_time_best = time_sorting_function(cocktail_shaker_sort, arr_for_cocktail_best)
        cocktail_times_best.append(cocktail_time_best)

    plt.figure(figsize=(12, 7))
    plt.plot(sizes, regular_times_worst, label="Regular Bubble Sort (Worst Case)", color='blue', marker='o')
    plt.plot(sizes, improved_times_worst, label="Improved Bubble Sort (Worst Case)", color='green', marker='o')
    plt.plot(sizes, cocktail_times_worst, label="Cocktail Shaker Sort (Worst Case)", color='red', marker='o')
    
    plt.plot(sizes, regular_times_avg, label="Regular Bubble Sort (Average)", color='purple', marker='s')
    plt.plot(sizes, improved_times_avg, label="Improved Bubble Sort (Average)", color='orange', marker='s')
    plt.plot(sizes, cocktail_times_avg, label="Cocktail Shaker Sort (Average)", color='brown', marker='s')
    
    plt.plot(sizes, regular_times_best, label="Regular Bubble Sort (Best Case)", color='cyan', marker='^')
    plt.plot(sizes, improved_times_best, label="Improved Bubble Sort (Best Case)", color='magenta', marker='^')
    plt.plot(sizes, cocktail_times_best, label="Cocktail Shaker Sort (Best Case)", color='yellow', marker='^')
    
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.title('Bubble Sort Performance Comparison')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    compare_and_plot()
