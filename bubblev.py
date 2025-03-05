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
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Sort Visualization")

# Font for text
font = pygame.font.Font(None, 36)

class BubbleSortVisualizer:
    def __init__(self, arr, delay=100):
        self.arr = arr
        self.delay = delay  # Delay between steps for visualization
        self.accesses = 0  # Counter for array accesses
        self.comparisons = 0  # Counter for comparisons

    def draw_array(self, screen, comparing=[], swapped=[], sorted_indices=[]):
        """Draw the current state of the array"""
        screen.fill(WHITE)
        
        # Calculate bar width and scaling
        bar_width = WIDTH // len(self.arr)
        max_height = max(self.arr)
        
        for i, val in enumerate(self.arr):
            # Calculate bar height
            bar_height = (val / max_height) * (HEIGHT - 100)
            
            # Determine bar color
            color = BLUE
            if i in comparing:
                color = GREEN  # Elements being compared in green
            if i in swapped:
                color = RED  # Recently swapped elements in red
            if i in sorted_indices:
                color = YELLOW  # Sorted elements in yellow
            
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
        accesses_text = font.render(f"Array Accesses: {self.accesses}", True, BLACK)
        comparisons_text = font.render(f"Comparisons: {self.comparisons}", True, BLACK)
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
        
    def bubble_sort(self):
        """Bubble Sort algorithm with visualization"""
        n = len(self.arr)
        
        # Traverse through all array elements
        for i in range(n):
            # Flag to optimize by breaking early if no swaps occur
            swapped = False
            
            # Last i elements are already in place, so we don't need to check them
            for j in range(0, n-i-1):
                # Visualize comparison
                self.comparisons += 1
                self.draw_array(screen, comparing=[j, j+1])
                
                # Swap if the element found is greater than the next element
                if self.arr[j] > self.arr[j+1]:
                    # Swap elements
                    self.arr[j], self.arr[j+1] = self.arr[j+1], self.arr[j]
                    
                    # Visualize swap
                    self.accesses += 2
                    self.draw_array(screen, swapped=[j, j+1])
                    
                    # Set swapped flag
                    swapped = True
            
            # If no swapping occurred, array is already sorted
            if not swapped:
                break
            
            # Highlight sorted portion at the end
            self.draw_array(screen, sorted_indices=range(n-i-1, n))
        
        # Final visualization of completely sorted array
        self.draw_array(screen, sorted_indices=range(len(self.arr)))
    
    def run_visualization(self):
        """Main visualization method"""
        # Initial draw of unsorted array
        self.draw_array(screen)
        
        # Run bubble sort
        self.bubble_sort()

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
            visualizer = BubbleSortVisualizer(arr, delay=time_delay)
            
            # Run visualization
            visualizer.run_visualization()
            start = False
        
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