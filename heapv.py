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
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heap Sort Visualization")

# Font for text
font = pygame.font.Font(None, 36)

class HeapSortVisualizer:
    def __init__(self, arr):
        self.arr = arr
        self.delay = 0.5  # Delay between steps for visualization
        
    def draw_array(self, screen, heapifying=[], comparing=[], sorted_indices=[]):
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
            if i in heapifying:
                color = ORANGE  # Heapifying elements in orange
            elif i in comparing:
                color = GREEN  # Elements being compared in green
            elif i in sorted_indices:
                color = PURPLE  # Sorted elements in purple
            
            # Draw the bar
            pygame.draw.rect(
                screen, 
                color, 
                (i * bar_width, HEIGHT - bar_height, bar_width, bar_height)
            )
        
        # Update the display
        pygame.display.flip()
        
        # Small delay to visualize the process
        pygame.time.delay(int(self.delay * 1000))
        
    def heapify(self, n, i):
        """Heapify a subtree rooted with node i"""
        largest = i  # Initialize largest as root
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Visualize initial state
        self.draw_array(screen, heapifying=[i, left, right], comparing=[largest])
        
        # See if left child of root exists and is greater than root
        if left < n and self.arr[left] > self.arr[largest]:
            largest = left
        
        # See if right child of root exists and is greater than largest so far
        if right < n and self.arr[right] > self.arr[largest]:
            largest = right
        
        # Change root, if needed
        if largest != i:
            # Swap
            self.arr[i], self.arr[largest] = self.arr[largest], self.arr[i]
            
            # Visualize swap
            self.draw_array(screen, heapifying=[i, largest])
            
            # Heapify the root
            self.heapify(n, largest)
    
    def heap_sort(self):
        """Heap sort algorithm"""
        n = len(self.arr)
        
        # Build a max-heap
        # Start from last non-leaf node and move upwards
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)
        
        # One by one extract elements
        for i in range(n - 1, 0, -1):
            # Move current root to end
            self.arr[0], self.arr[i] = self.arr[i], self.arr[0]
            
            # Visualize extraction
            self.draw_array(screen, sorted_indices=[i], heapifying=[0])
            
            # Call heapify on the reduced heap
            self.heapify(i, 0)
        
        # Final visualization of completely sorted array
        self.draw_array(screen, sorted_indices=range(len(self.arr)))
    
    def run_visualization(self):
        """Main visualization method"""
        # Initial draw of unsorted array
        self.draw_array(screen)
        
        # Run heap sort
        self.heap_sort()
        
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
def main():
    # Generate random array
    arr = generate_array()
    
    # Create visualizer
    visualizer = HeapSortVisualizer(arr)
    
    # Run visualization
    visualizer.run_visualization()

if __name__ == "__main__":
    main()