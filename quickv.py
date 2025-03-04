import pygame
import random

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

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quicksort Visualization")

# Font for text
font = pygame.font.Font(None, 36)

class QuicksortVisualizer:
    def __init__(self, arr, delay=100):
        self.arr = arr
        self.delay = delay  # Delay between steps for visualization
        self.accesses = 0  # Counter for array accesses
        self.comparisons = 0  # Counter for comparisons
        
    def draw_array(self, screen, comparisons=[], pivots=[], sorted_indices=[]):
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
            if i in pivots:
                color = RED  # Pivot elements in red
            elif i in comparisons:
                color = GREEN  # Elements being compared in green
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
        
        # Display counters
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

        
    def partition(self, low, high):
        """Partition the array and return the pivot index"""
        # Choose the rightmost element as pivot
        pivot = self.arr[high]
        self.accesses += 1
        
        # Pointer for greater element
        i = low - 1
        
        # Traverse through all elements
        # Compare each element with pivot
        for j in range(low, high):
            self.accesses += 1
            self.comparisons += 1
            # Draw current state
            self.draw_array(screen, comparisons=[j, high], pivots=[high])
            
            # If element smaller than pivot is found
            if self.arr[j] <= pivot:
                # Increment index of smaller element
                i += 1
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
                self.accesses += 2
        
        # Place the pivot in the correct position
        self.arr[i + 1], self.arr[high] = self.arr[high], self.arr[i + 1]
        self.accesses += 2
        
        # Draw final state of this partition
        self.draw_array(screen, pivots=[i+1])
        
        return i + 1
    
    def quicksort(self, low, high):       
        """Recursive quicksort implementation"""
        if low < high:
            # Find pivot element such that 
            # elements smaller than pivot are on the left
            # elements greater than pivot are on the right
            pi = self.partition(low, high)
            
            # Recursive call on the left of pivot
            self.quicksort(low, pi - 1)
            
            # Recursive call on the right of pivot
            self.quicksort(pi + 1, high)
        
        # When sorting is complete, highlight entire array
        if low == 0 and high == len(self.arr) - 1:
            self.draw_array(screen, sorted_indices=range(len(self.arr)))
    
    def run_visualization(self):
        """Main visualization method"""
        self.draw_array(screen)
        
        self.quicksort(0, len(self.arr) - 1)
               # Keep final screen open
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.quit()
        
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
            visualizer = QuicksortVisualizer(arr, delay=time_delay)
            
            # Run visualization
            visualizer.run_visualization()
            start = False
        
        pygame.display.flip()
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
