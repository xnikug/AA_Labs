import random
import time
import matplotlib.pyplot as plt
import sys

# Regular Merge Sort
def merge_sort(arr):
    """
    Standard merge sort implementation
    """
    # Base case
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # Recursively sort both halves
    left = merge_sort(left)
    right = merge_sort(right)
    
    # Merge
    return merge(left, right)

def merge(left, right):
    """
    Merge two sorted lists
    """
    result = []
    i = j = 0
    
    # Compare and merge
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

# Improved Merge Sort with Insertion Sort for Small Partitions
def improved_merge_sort(arr):
    """
    Improved merge sort with insertion sort for small arrays
    """
    def insertion_sort(arr):
        """
        Insertion sort for small partitions
        """
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    
    # Threshold for switching to insertion sort
    INSERTION_SORT_THRESHOLD = 16
    
    def _merge_sort(arr):
        # Base case with insertion sort for small arrays
        if len(arr) <= INSERTION_SORT_THRESHOLD:
            return insertion_sort(arr)
        
        # Divide
        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        
        # Merge with additional optimization
        return merge_optimized(left, right)
    
    def merge_optimized(left, right):
        """
        Optimized merge with early termination and reduced comparisons
        """
        # If last element of left is <= first element of right, 
        # arrays are already sorted
        if left[-1] <= right[0]:
            return left + right
        
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Add remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    return _merge_sort(arr)

# Function to time the sorting process
def time_sorting_function(sort_func, arr):
    start_time = time.time()
    sort_func(arr)
    return time.time() - start_time

# Main function to compare and plot results
def compare_and_plot():
    # Increased array sizes for more comprehensive comparison
    sizes = [10, 100, 300, 1000, 2000, 3000, 5000, 10000]
    
    # Lists to store timing results
    regular_times_worst = []
    improved_times_worst = []
    regular_times_avg = []
    improved_times_avg = []
    
    for size in sizes:
        # Reversed sorted array
        arr_for_regular_worst = list(range(size, 0, -1))
        arr_for_improved_worst = arr_for_regular_worst.copy()
        
        # Average case: Random array
        arr_for_regular_avg = [random.randint(1, size * 10) for _ in range(size)]
        arr_for_improved_avg = arr_for_regular_avg.copy()

        # Time regular merge sort (reversed sorted array)
        regular_time_worst = time_sorting_function(merge_sort, arr_for_regular_worst)
        regular_times_worst.append(regular_time_worst)

        # Time improved merge sort (reversed sorted array)
        improved_time_worst = time_sorting_function(improved_merge_sort, arr_for_improved_worst)
        improved_times_worst.append(improved_time_worst)

        # Time regular merge sort (average case)
        regular_time_avg = time_sorting_function(merge_sort, arr_for_regular_avg)
        regular_times_avg.append(regular_time_avg)

        # Time improved merge sort (average case)
        improved_time_avg = time_sorting_function(improved_merge_sort, arr_for_improved_avg)
        improved_times_avg.append(improved_time_avg)

    # Plotting the results
    plt.figure(figsize=(12, 7))
    plt.plot(sizes, regular_times_worst, label="Regular Merge Sort (Reversed Array Case)", color='blue', marker='o')
    plt.plot(sizes, improved_times_worst, label="Improved Merge Sort (Reversed Array Case)", color='green', marker='o')
    plt.plot(sizes, regular_times_avg, label="Regular Merge Sort (Random)", color='purple', marker='o')
    plt.plot(sizes, improved_times_avg, label="Improved Merge Sort (Random)", color='red', marker='o')
    
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.title('Merge Sort Performance Comparison')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')  # Use log scale for better visualization
    plt.tight_layout()
    plt.show()

# Run the comparison and plotting
if __name__ == "__main__":

    compare_and_plot()