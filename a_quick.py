import random
import time
import matplotlib.pyplot as plt
import sys
# Regular Quick Sort
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]  # Choosing the last element as the pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Median-of-three Quick Sort (Improved)
def median_of_three(arr, low, high):
    mid = (low + high) // 2
    a = arr[low]
    b = arr[mid]
    c = arr[high]
    
    if a < b:
        if b < c:
            return mid
        elif a < c:
            return high
        else:
            return low
    else:
        if a < c:
            return low
        elif b < c:
            return high
        else:
            return mid

def quicksort_improved(arr, low, high):
    if low < high:
        pivot_index = median_of_three(arr, low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]
        
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        quicksort_improved(arr, low, i)
        quicksort_improved(arr, i + 2, high)

def improved_quick_sort(arr):
    quicksort_improved(arr, 0, len(arr) - 1)
    return arr

# Function to time the sorting process
def time_sorting_function(sort_func, arr):
    start_time = time.time()
    sort_func(arr)
    return time.time() - start_time

# Main function to compare and plot results
def compare_and_plot():
    sizes = [10, 100, 300, 1000, 2000, 3000]  # Sizes of the random arrays
    regular_times = []
    improved_times = []
    regular_times_avg = []
    improved_times_avg = []
    for size in sizes:
        arr_for_regular = [e for e in range(1, size)]  # On a reversed sorted array
        arr_for_improved = arr_for_regular.copy()  # Copy to ensure same input for both
        arr_for_regular_avg = [random.randint(1, size) for _ in range(size)]  # On a random array
        arr_for_improved_avg = arr_for_regular_avg.copy()  # Copy to ensure same input for both

        # Time regular quicksort
        regular_time = time_sorting_function(quicksort, arr_for_regular)
        regular_times.append(regular_time)

        # Time improved quicksort
        improved_time = time_sorting_function(improved_quick_sort, arr_for_improved)
        improved_times.append(improved_time)

        # Time regular quicksort average case
        regular_time_avg = time_sorting_function(quicksort, arr_for_regular_avg)
        regular_times_avg.append(regular_time_avg)

        # Time improved quicksort average case
        improved_time_avg = time_sorting_function(improved_quick_sort, arr_for_improved_avg)
        improved_times_avg.append(improved_time_avg)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, regular_times, label="Regular QuickSort (Worst Case)", color='blue', marker='o')
    plt.plot(sizes, improved_times, label="Improved QuickSort (Worst Case)", color='green', marker='o')
    plt.plot(sizes, regular_times_avg, label="Regular QuickSort (Average)", color='purple', marker='o')
    plt.plot(sizes, improved_times_avg, label="Improved QuickSort (Average)", color='red', marker='o')
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.title('QuickSort Performance Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()


# Run the comparison and plotting
if __name__ == "__main__":
    sys.setrecursionlimit(1000000)

    compare_and_plot()
