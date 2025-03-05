import random
import time
import matplotlib.pyplot as plt

# Heap Sort using Floyd's Heap Construction Algorithm
def heap_sort_floyd(arr):

    def floyd_heapify(arr, n, i):

        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        while True:
            # Find the largest among root, left child, and right child
            max_index = largest
            
            if left < n and arr[left] > arr[max_index]:
                max_index = left
            
            if right < n and arr[right] > arr[max_index]:
                max_index = right
            
            # If root is largest, we're done
            if max_index == largest:
                break
            
            # Swap and continue heapifying
            arr[largest], arr[max_index] = arr[max_index], arr[largest]
            
            # Update indices for next iteration
            largest = max_index
            left = 2 * largest + 1
            right = 2 * largest + 2
    
    # Create a copy to avoid modifying the original array
    arr = arr.copy()
    
    n = len(arr)
    
    # Floyd's algorithm for heap construction
    # Start from the last non-leaf node and move upwards
    for i in range(n // 2 - 1, -1, -1):
        floyd_heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]
        
        # Heapify the reduced heap
        floyd_heapify(arr, i, 0)
    
    return arr

# Improved Heap Sort with Floyd's algorithm and additional optimizations
def improved_heap_sort_floyd(arr):

    def floyd_heapify_optimized(arr, n, i):

        # Store the root value
        root = arr[i]
        
        # Start with root index
        largest = i
        
        while True:
            left = 2 * largest + 1
            right = 2 * largest + 2
            
            # Find the largest child
            max_child = largest
            
            if left < n and arr[left] > arr[max_child]:
                max_child = left
            
            if right < n and arr[right] > arr[max_child]:
                max_child = right
            
            # If no larger child found, restore root and break
            if max_child == largest:
                arr[largest] = root
                break
            
            # Move child up
            arr[largest] = arr[max_child]
            largest = max_child
        
    # Create a copy to avoid modifying the original array
    arr = arr.copy()
    
    n = len(arr)
    
    # Floyd's algorithm with optimization
    # Use bottom-up construction with minimized swapping
    for i in range(n // 2 - 1, -1, -1):
        floyd_heapify_optimized(arr, n, i)
    
    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        # Store the root (maximum element)
        max_element = arr[0]
        
        # Rebuild heap from top
        floyd_heapify_optimized(arr, i, 0)
        
        # Place the maximum element at the end
        arr[i] = max_element
    
    return arr

# Function to time the sorting process
def time_sorting_function(sort_func, arr):
    start_time = time.time()
    sort_func(arr)
    return time.time() - start_time

# Main function to compare and plot results
def compare_and_plot():
    # Increased array sizes for more comprehensive comparison
    sizes = [10, 100, 300, 1000, 2000, 3000, 5000, 10000, 20000, 50000]
    
    # Lists to store timing results
    regular_times_worst = []
    improved_times_worst = []
    regular_times_avg = []
    improved_times_avg = []
    
    for size in sizes:
        # Worst case: Reversed sorted array
        arr_for_regular_worst = list(range(size, 0, -1))
        arr_for_improved_worst = arr_for_regular_worst.copy()
        
        # Average case: Random array
        arr_for_regular_avg = [random.randint(1, size * 10) for _ in range(size)]
        arr_for_improved_avg = arr_for_regular_avg.copy()

        # Time regular heap sort (worst case)
        regular_time_worst = time_sorting_function(heap_sort_floyd, arr_for_regular_worst)
        regular_times_worst.append(regular_time_worst)

        # Time improved heap sort (worst case)
        improved_time_worst = time_sorting_function(improved_heap_sort_floyd, arr_for_improved_worst)
        improved_times_worst.append(improved_time_worst)

        # Time regular heap sort (average case)
        regular_time_avg = time_sorting_function(heap_sort_floyd, arr_for_regular_avg)
        regular_times_avg.append(regular_time_avg)

        # Time improved heap sort (average case)
        improved_time_avg = time_sorting_function(improved_heap_sort_floyd, arr_for_improved_avg)
        improved_times_avg.append(improved_time_avg)

    # Plotting the results
    plt.figure(figsize=(12, 7))
    plt.plot(sizes, regular_times_worst, label="Regular Heap Sort (Reversed Array Case)", color='blue', marker='o')
    plt.plot(sizes, improved_times_worst, label="Improved Heap Sort (Reversed Array Case)", color='green', marker='o')
    plt.plot(sizes, regular_times_avg, label="Regular Heap Sort (Random)", color='purple', marker='o')
    plt.plot(sizes, improved_times_avg, label="Improved Heap Sort (Random)", color='red', marker='o')
    
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.title('Heap Sort Performance Comparison (Floyd\'s Algorithm)')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')  # Use log scale for better visualization
    plt.tight_layout()
    plt.show()

# Run the comparison and plotting
if __name__ == "__main__":

    compare_and_plot()