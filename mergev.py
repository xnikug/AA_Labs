import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merge Sort Visualization")

# Font for text
font = pygame.font.Font(None, 36)

class MergeSortVisualizer:
    def __init__(self, arr, delay=100):
        self.arr = arr
        self.delay = delay  # Delay between steps for visualization
        self.accesses = 0
        self.comparisons = 0
        
    def draw_array(self, screen, comparisons=[], merging_sections=[], sorted_indices=[]):
        """Draw the current state of the array"""
        screen.fill(BLACK)
        
        # Calculate bar width and scaling
        bar_width = WIDTH // len(self.arr)
        max_height = max(self.arr)
        
        for i, val in enumerate(self.arr):
            # Calculate bar height
            bar_height = (val / max_height) * (HEIGHT - 100)
            
            # Determine bar color
            color = BLUE
            if i in comparisons:
                color = GREEN  # Elements being compared in green
            elif i in merging_sections:
                color = RED  # Sections being merged in red
            elif i in sorted_indices:
                color = (100, 200, 100)  # Sorted elements in a lighter green

            # Draw the bar
            pygame.draw.rect(
                screen, 
                pygame.Color("white"), 
                (i * bar_width, HEIGHT - bar_height, bar_width, bar_height)
            )
            pygame.draw.rect(
                screen, 
                color, 
                (i * bar_width + 1, HEIGHT - bar_height + 1, bar_width - 2, bar_height - 2)
            )
        
        # Draw counters
        accesses_text = font.render(f"Array Accesses: {self.accesses}", True, WHITE)
        comparisons_text = font.render(f"Comparisons: {self.comparisons}", True, WHITE)
        screen.blit(accesses_text, (10, 10))
        screen.blit(comparisons_text, (10, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        # Update the display
        pygame.display.flip()
        
        # Small delay to visualize the process
        pygame.time.delay(int(self.delay))
        
    def merge(self, left, mid, right):
        """Merge two sorted subarrays"""
        # Create temp arrays
        left_half = self.arr[left:mid+1]
        right_half = self.arr[mid+1:right+1]
        
        # Initial indices
        i = j = 0
        k = left
        
        # Merge the temp arrays
        while i < len(left_half) and j < len(right_half):
            # Visualize comparison
            self.comparisons += 1
            self.draw_array(
                screen, 
                comparisons=[
                    left + i, 
                    mid + 1 + j
                ],
                merging_sections=list(range(left, right+1))
            )
            
            if left_half[i] <= right_half[j]:
                self.arr[k] = left_half[i]
                i += 1
            else:
                self.arr[k] = right_half[j]
                j += 1
            self.accesses += 1
            k += 1
        
        # Check for any remaining elements
        while i < len(left_half):
            self.arr[k] = left_half[i]
            i += 1
            k += 1
            self.accesses += 1
        
        while j < len(right_half):
            self.arr[k] = right_half[j]
            j += 1
            k += 1
            self.accesses += 1
        
        # Visualize merged section
        self.draw_array(
            screen, 
            merging_sections=list(range(left, right+1))
        )
    
    def merge_sort(self, left, right):
        """Recursive merge sort implementation"""
        if left < right:
            # Find the middle point
            mid = (left + right) // 2
            
            # Recursively sort first and second halves
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            
            # Merge the sorted halves
            self.merge(left, mid, right)
        
        # When sorting is complete, highlight entire array
        if left == 0 and right == len(self.arr) - 1:
            self.draw_array(screen, sorted_indices=range(len(self.arr)))
    
    def run_visualization(self):
        """Main visualization method"""
        # Initial draw of unsorted array
        self.draw_array(screen)
        
        # Run merge sort
        self.merge_sort(0, len(self.arr) - 1)
        
# Generate random array
def generate_array(size=50, min_val=10, max_val=500):
    return [random.randint(min_val, max_val) for _ in range(size)]

# Main execution
def input_params():
    array_size = int(input("Enter the size of the array(default is 50): ") or 50)
    if array_size > 200 or array_size < 1:
        raise ValueError("Array size should be between 1 and 200")
    time_delay = int(input("Enter the time delay between steps(ms): ") or 100)
    if time_delay > 10000 or time_delay < 1:
        raise ValueError("Time delay should be between 1ms and 10000ms")
    return array_size, time_delay
def main():
    array_size, time_delay = input_params()
    start = True
    while True:
        if start:
            # Generate random array
            arr = generate_array(array_size)
            
            # Create visualizer
            visualizer = MergeSortVisualizer(arr, delay=time_delay)
            
            # Run visualization
            visualizer.run_visualization()
            start = False
        
        #pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    array_size, time_delay = input_params()
                    start = True


if __name__ == "__main__":
    main()