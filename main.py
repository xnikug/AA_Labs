import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from collections import deque
import os

# Create directory for saving frames
os.makedirs("traversal_frames", exist_ok=True)

# Create a sample graph with interesting structure for visualization
def create_sample_graph():
    """Create a sample graph with a mix of features to demonstrate traversal differences"""
    G = nx.Graph()
    
    # Add nodes
    for i in range(1, 16):  # 15 nodes
        G.add_node(i)
    
    # Add edges to create an interesting structure with multiple paths and branches
    edges = [
        (1, 2), (1, 3), (1, 4),  # Node 1 connects to 2, 3, and 4
        (2, 5), (2, 6),          # Node 2 connects to 5 and 6
        (3, 7), (3, 8),          # Node 3 connects to 7 and 8
        (4, 9),                  # Node 4 connects to 9
        (5, 10),                 # Node 5 connects to 10
        (7, 11), (7, 12),        # Node 7 connects to 11 and 12
        (9, 13), (9, 14),        # Node 9 connects to 13 and 14
        (10, 6),                 # Connect 10 back to 6 to create a cycle
        (12, 15),                # Node 12 connects to 15
        (13, 15),                # Node 13 also connects to 15
        (6, 8)                   # Connect 6 to 8 to create another cycle
    ]
    G.add_edges_from(edges)
    
    return G

def dfs_steps(G, start):
    """Generate step-by-step DFS traversal"""
    visited = set()
    stack = [start]
    traversal = []
    edges_used = []
    
    while stack:
        node = stack[-1]  # Look at the top of the stack
        
        if node not in visited:
            visited.add(node)
            traversal.append(node)
            stack.pop()  # Remove current node from stack
            
            # Add unvisited neighbors to stack (in reverse order for correct DFS)
            neighbors = sorted(list(G.neighbors(node)), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
                    edges_used.append((node, neighbor))
        else:
            stack.pop()  # Node already visited, just remove it
    
    return traversal, edges_used

def bfs_steps(G, start):
    """Generate step-by-step BFS traversal"""
    visited = set([start])
    queue = deque([start])
    traversal = [start]
    edges_used = []
    
    while queue:
        node = queue.popleft()
        
        # Add unvisited neighbors to queue
        neighbors = sorted(list(G.neighbors(node)))
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                traversal.append(neighbor)
                queue.append(neighbor)
                edges_used.append((node, neighbor))
    
    return traversal, edges_used

def create_traversal_animation(G, algorithm, start_node, title):
    """Create animation frames showing a traversal algorithm in action"""
    if algorithm == "DFS":
        traversal, edges_used = dfs_steps(G, start_node)
        color = "red"
        cmap_name = "Reds"
    else:  # BFS
        traversal, edges_used = bfs_steps(G, start_node)
        color = "blue"
        cmap_name = "Blues"
    
    # Create a layout for the graph (consistent for both algorithms)
    pos = nx.spring_layout(G, seed=42)
    
    # Create a custom colormap that goes from white to the algorithm color
    cmap = LinearSegmentedColormap.from_list(f"White_to_{color}", ["white", color], N=len(traversal))
    
    # Save static image with initial state
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color="white", 
            node_size=700, font_size=16, font_weight="bold",
            edgecolors="black", linewidths=1)
    plt.title(f"{algorithm} Traversal - Initial State", fontsize=16)
    plt.savefig(f"traversal_frames/{algorithm}_initial.png")
    plt.close()
    
    # Generate and save frames for each step
    edges_traversed = set()
    for i, node in enumerate(traversal):
        plt.figure(figsize=(10, 8))
        
        # Add edges that have been traversed at this step
        if i < len(edges_used):
            edges_traversed.add(edges_used[i])
        
        # Draw the graph with the current traversal state
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.3)
        nx.draw_networkx_edges(G, pos, edgelist=list(edges_traversed), 
                              width=2, edge_color=color, alpha=0.7)
        
        # Color all nodes visited so far
        node_colors = ["white"] * len(G.nodes())
        for j, visited_node in enumerate(traversal[:i+1]):
            node_idx = list(G.nodes()).index(visited_node)
            node_colors[node_idx] = cmap(j / len(traversal))
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=700, edgecolors="black", linewidths=1)
        
        # Highlight the current node
        nx.draw_networkx_nodes(G, pos, nodelist=[node], 
                              node_color=color, node_size=700, 
                              edgecolors="black", linewidths=2)
        
        # Add node labels
        nx.draw_networkx_labels(G, pos, font_size=16, font_weight="bold")
        
        # Add traversal order
        for j, visited_node in enumerate(traversal[:i+1]):
            x, y = pos[visited_node]
            plt.text(x + 0.1, y + 0.1, f"({j+1})", fontsize=12, 
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        plt.title(f"{algorithm} Traversal - Step {i+1}: Visit Node {node}", fontsize=16)
        plt.savefig(f"traversal_frames/{algorithm}_step_{i+1:02d}.png")
        plt.close()
    
    # Save final state with complete traversal
    plt.figure(figsize=(10, 8))
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.3)
    nx.draw_networkx_edges(G, pos, edgelist=list(edges_traversed), 
                          width=2, edge_color=color)
    
    # Color nodes according to visit order
    node_colors = ["white"] * len(G.nodes())
    for i, node in enumerate(traversal):
        node_idx = list(G.nodes()).index(node)
        node_colors[node_idx] = cmap(i / len(traversal))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=700, edgecolors="black", linewidths=1)
    
    # Add node labels
    nx.draw_networkx_labels(G, pos, font_size=16, font_weight="bold")
    
    # Add traversal order labels
    for i, node in enumerate(traversal):
        x, y = pos[node]
        plt.text(x + 0.1, y + 0.1, f"({i+1})", fontsize=12, 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.title(f"{algorithm} Traversal - Complete ({len(traversal)} nodes)", fontsize=16)
    plt.savefig(f"traversal_frames/{algorithm}_final.png")
    plt.close()
    
    return traversal

def create_side_by_side_comparison(G, dfs_traversal, bfs_traversal):
    """Create a side-by-side comparison of DFS and BFS traversal order"""
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(15, 8))
    
    # DFS subplot
    plt.subplot(1, 2, 1)
    dfs_cmap = LinearSegmentedColormap.from_list("White_to_red", ["white", "red"], N=len(dfs_traversal))
    
    # Color nodes according to DFS visit order
    node_colors = ["white"] * len(G.nodes())
    for i, node in enumerate(dfs_traversal):
        node_idx = list(G.nodes()).index(node)
        node_colors[node_idx] = dfs_cmap(i / len(dfs_traversal))
    
    # Draw DFS graph
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=700, font_size=12, font_weight="bold",
            edgecolors="black", linewidths=1)
    
    # Add DFS traversal order
    for i, node in enumerate(dfs_traversal):
        x, y = pos[node]
        plt.text(x + 0.1, y + 0.1, f"({i+1})", fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.title("DFS Traversal Order", fontsize=16)
    
    # BFS subplot
    plt.subplot(1, 2, 2)
    bfs_cmap = LinearSegmentedColormap.from_list("White_to_blue", ["white", "blue"], N=len(bfs_traversal))
    
    # Color nodes according to BFS visit order
    node_colors = ["white"] * len(G.nodes())
    for i, node in enumerate(bfs_traversal):
        node_idx = list(G.nodes()).index(node)
        node_colors[node_idx] = bfs_cmap(i / len(bfs_traversal))
    
    # Draw BFS graph
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=700, font_size=12, font_weight="bold",
            edgecolors="black", linewidths=1)
    
    # Add BFS traversal order
    for i, node in enumerate(bfs_traversal):
        x, y = pos[node]
        plt.text(x + 0.1, y + 0.1, f"({i+1})", fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.title("BFS Traversal Order", fontsize=16)
    
    plt.tight_layout()
    plt.savefig("traversal_frames/dfs_bfs_comparison.png", dpi=300)
    plt.close()

def create_traversal_tables(dfs_traversal, bfs_traversal):
    """Create a table showing the traversal order for both algorithms"""
    data = []
    for i in range(max(len(dfs_traversal), len(bfs_traversal))):
        dfs_node = dfs_traversal[i] if i < len(dfs_traversal) else "-"
        bfs_node = bfs_traversal[i] if i < len(bfs_traversal) else "-"
        data.append([i+1, dfs_node, bfs_node])
    
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=data, 
                    colLabels=["Step", "DFS Node", "BFS Node"],
                    colWidths=[0.2, 0.4, 0.4],
                    cellLoc='center',
                    loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    
    # Add colors to the table headers
    table[(0, 1)].set_facecolor('#ffcccc')  # Light red for DFS
    table[(0, 2)].set_facecolor('#cce5ff')  # Light blue for BFS
    
    plt.title("DFS vs BFS Traversal Order", fontsize=16)
    plt.savefig("traversal_frames/traversal_table.png", dpi=300, bbox_inches='tight')
    plt.close()
from PIL import Image
import os

def create_gif_from_images(images_list, output_filename, duration=500):
    """
    Create a GIF from a list of image paths.
    
    Args:
        images_list: List of image file paths
        output_filename: Name of the GIF file to create
        duration: Duration for each frame in milliseconds (default: 500)
    """
    # Check if all files exist before attempting to create GIF
    missing_files = [img for img in images_list if not os.path.exists(img)]
    if missing_files:
        print(f"Error: The following files are missing: {missing_files}")
        return False
    
    # Open all images
    frames = []
    for image_file in images_list:
        try:
            frame = Image.open(image_file)
            frames.append(frame.copy())  # Create a copy to avoid issues with closed files
        except Exception as e:
            print(f"Error opening {image_file}: {e}")
            return False
    
    # Save as GIF
    if frames:
        try:
            frames[0].save(
                output_filename,
                format="GIF",
                append_images=frames[1:],
                save_all=True,
                duration=duration,
                loop=0,  # 0 means loop forever
                optimize=True
            )
            print(f"GIF created successfully as '{output_filename}'.")
            return True
        except Exception as e:
            print(f"Error creating GIF: {e}")
            return False
    else:
        print("No frames to create GIF.")
        return False
def main():
    # Create a sample graph
    G = create_sample_graph()
    
    # Starting node for traversals
    start_node = 1
    
    # Generate DFS traversal and animation
    print("Generating DFS visualization...")
    dfs_traversal = create_traversal_animation(G, "DFS", start_node, "Depth-First Search")
    
    # Generate BFS traversal and animation
    print("Generating BFS visualization...")
    bfs_traversal = create_traversal_animation(G, "BFS", start_node, "Breadth-First Search")
    
    # Create side-by-side comparison
    print("Creating side-by-side comparison...")
    create_side_by_side_comparison(G, dfs_traversal, bfs_traversal)
    
    # Create traversal order tables
    print("Creating traversal order table...")
    create_traversal_tables(dfs_traversal, bfs_traversal)
    
    print("Visualization complete! Images saved in 'traversal_frames' directory.")
    print(f"DFS traversal order: {dfs_traversal}")
    print(f"BFS traversal order: {bfs_traversal}")
    # Optionally, you can create a GIF from the saved frames
    # Uncomment the following lines to create a GIF from the frames
    # Create DFS animation
    dfs_images = []
    # Start with initial state
    dfs_images.append("traversal_frames/DFS_initial.png")
    # Add each step in the traversal
    for i in range(1, len(dfs_traversal) + 1):
        dfs_images.append(f"traversal_frames/DFS_step_{i:02d}.png")
    # Add final state
    dfs_images.append("traversal_frames/DFS_final.png")

    # Create BFS animation
    bfs_images = []
    # Start with initial state
    bfs_images.append("traversal_frames/BFS_initial.png")
    # Add each step in the traversal
    for i in range(1, len(bfs_traversal) + 1):
        bfs_images.append(f"traversal_frames/BFS_step_{i:02d}.png")
    # Add final state
    bfs_images.append("traversal_frames/BFS_final.png")

    # Create the GIFs
    create_gif_from_images(dfs_images, "dfs_traversal.gif", duration=800)
    create_gif_from_images(bfs_images, "bfs_traversal.gif", duration=800)
    
if __name__ == "__main__":
    main()