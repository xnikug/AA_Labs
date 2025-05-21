import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import to_rgba
import matplotlib.cm as cm
from copy import deepcopy
import os

# Create a sample directed graph with weighted edges
def create_sample_graph():
    G = nx.DiGraph()
    
    # Add nodes
    for i in range(6):
        G.add_node(i)
    
    # Add weighted edges
    edges = [
        (0, 1, 7), (0, 2, 9), (0, 5, 14),
        (1, 2, 10), (1, 3, 15),
        (2, 3, 11), (2, 5, 2),
        (3, 4, 6),
        (4, 5, 9)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    
    return G

# Set fixed positions for the nodes for consistent layout
def get_node_positions(G):
    pos = {
        0: (0, 0),
        1: (1, 1),
        2: (2, 0),
        3: (3, 1),
        4: (4, 0),
        5: (2, -1)
    }
    return pos

# ------------ FLOYD-WARSHALL VISUALIZATION ------------

def floyd_warshall_animation(G):
    # Initialize distance matrix
    nodes = list(G.nodes())
    n = len(nodes)
    
    # Create a mapping from node labels to indices
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    
    # Initialize distance matrix with infinity
    dist = np.full((n, n), np.inf)
    
    # Set distance from a node to itself as 0
    for i in range(n):
        dist[i, i] = 0
    
    # Set distance for direct edges
    for u, v, data in G.edges(data=True):
        dist[node_to_idx[u], node_to_idx[v]] = data['weight']
    
    # Store the state at each step for animation
    states = []
    states.append(deepcopy(dist))
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i, k] + dist[k, j] < dist[i, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]
        states.append(deepcopy(dist))
    
    return states, nodes, node_to_idx

def animate_floyd_warshall(G):
    states, nodes, node_to_idx = floyd_warshall_animation(G)
    n = len(nodes)
    pos = get_node_positions(G)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle("Floyd-Warshall Algorithm Visualization", fontsize=16)
    
    # Function to update the graph and distance matrix visualization
    def update(frame):
        ax1.clear()
        ax2.clear()
        
        # Draw the graph
        nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=500, node_color='lightblue')
        
        # Special highlighting for the current intermediate node
        if frame > 0:
            k = frame - 1
            nx.draw_networkx_nodes(G, pos, nodelist=[nodes[k]], ax=ax1, node_size=500, node_color='red')
        
        # Draw the edges
        edge_colors = []
        edge_widths = []
        
        for u, v, data in G.edges(data=True):
            edge_colors.append('black')
            edge_widths.append(1)
        
        nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=list(G.edges()), 
                               edge_color=edge_colors, width=edge_widths, 
                               connectionstyle='arc3,rad=0.1', arrowsize=15)
        
        # Draw edge labels
        edge_labels = {(u, v): data['weight'] for u, v, data in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1, font_size=10)
        
        # Draw node labels
        nx.draw_networkx_labels(G, pos, ax=ax1, font_size=12)
        
        # Set axis title based on frame
        if frame == 0:
            ax1.set_title("Initial Graph")
        else:
            ax1.set_title(f"Intermediate node k={nodes[frame-1]}")
        
        # Display distance matrix
        dist_matrix = states[frame]
        ax2.set_title("Distance Matrix")
        ax2.set_xticks(range(n))
        ax2.set_yticks(range(n))
        ax2.set_xticklabels(nodes)
        ax2.set_yticklabels(nodes)
        
        # Set up the table colors - use a different color for infinity
        table_colors = np.empty((n, n), dtype=object)
        norm = plt.Normalize(1, max(1, np.max(dist_matrix[~np.isinf(dist_matrix)])))
        
        for i in range(n):
            for j in range(n):
                if np.isinf(dist_matrix[i, j]):
                    table_colors[i, j] = 'white'  # infinity color
                else:
                    # Use a color map for regular values
                    val = dist_matrix[i, j]
                    intensity = norm(max(1, val))
                    table_colors[i, j] = cm.Blues(intensity)
        
        # Create a custom table with colored cells
        cell_text = []
        for i in range(n):
            row = []
            for j in range(n):
                if np.isinf(dist_matrix[i, j]):
                    row.append("∞")
                else:
                    row.append(str(int(dist_matrix[i, j])))
            cell_text.append(row)
        
        table = ax2.table(cellText=cell_text, cellColours=table_colors, cellLoc='center',
                         loc='center', bbox=[0.1, 0.1, 0.8, 0.8])
        
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)
        
        ax2.axis('off')
    
    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(states), interval=1000, repeat=True)
    
    plt.tight_layout()
    plt.close()  # This prevents the figure from being displayed directly
    
    return ani

# ------------ DIJKSTRA VISUALIZATION ------------

def dijkstra_animation(G, source=0):
    # Get the nodes and prepare the distance and predecessor dictionaries
    nodes = list(G.nodes())
    dist = {node: float('infinity') for node in nodes}
    pred = {node: None for node in nodes}
    visited = set()
    
    dist[source] = 0
    
    # Store the states for animation
    states = []
    states.append((deepcopy(dist), deepcopy(pred), deepcopy(visited)))
    
    # Dijkstra's algorithm
    while len(visited) < len(nodes):
        # Find the node with minimum distance that is not yet visited
        min_dist = float('infinity')
        min_node = None
        for node in nodes:
            if node not in visited and dist[node] < min_dist:
                min_dist = dist[node]
                min_node = node
        
        # If no reachable node is found, break
        if min_node is None:
            break
        
        # Mark the minimum distance node as visited
        visited.add(min_node)
        
        # Update distances to neighbors
        for neighbor in G.neighbors(min_node):
            if neighbor not in visited:
                weight = G[min_node][neighbor]['weight']
                alt_dist = dist[min_node] + weight
                if alt_dist < dist[neighbor]:
                    dist[neighbor] = alt_dist
                    pred[neighbor] = min_node
        
        # Save the current state
        states.append((deepcopy(dist), deepcopy(pred), deepcopy(visited)))
    
    return states

def animate_dijkstra(G, source=0):
    states = dijkstra_animation(G, source)
    pos = get_node_positions(G)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.suptitle("Dijkstra's Algorithm Visualization", fontsize=16)
    
    # Function to update the graph visualization
    def update(frame):
        ax.clear()
        
        dist, pred, visited = states[frame]
        
        # Draw the graph
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            if node == source:
                node_colors.append('green')  # Source node
                node_sizes.append(700)
            elif node in visited:
                node_colors.append('red')  # Visited node
                node_sizes.append(600)
            else:
                node_colors.append('lightblue')  # Unvisited node
                node_sizes.append(500)
        
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes)
        
        # Draw the edges
        edge_colors = []
        edge_widths = []
        
        for u, v, data in G.edges(data=True):
            if u in visited and v in visited and pred[v] == u:
                # Edge is part of the shortest path
                edge_colors.append('red')
                edge_widths.append(3)
            elif u in visited and v in visited:
                # Edge between visited nodes but not in shortest path
                edge_colors.append('gray')
                edge_widths.append(1)
            else:
                # Regular edge
                edge_colors.append('black')
                edge_widths.append(1)
        
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=list(G.edges()), 
                               edge_color=edge_colors, width=edge_widths, 
                               connectionstyle='arc3,rad=0.1', arrowsize=15)
        
        # Draw edge labels
        edge_labels = {(u, v): data['weight'] for u, v, data in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=10)
        
        # Draw node labels with distances
        labels = {}
        for node in G.nodes():
            if dist[node] == float('infinity'):
                labels[node] = f"{node}\n(∞)"
            else:
                labels[node] = f"{node}\n({dist[node]})"
        
        nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=12)
        
        # Set the title based on the frame
        if frame == 0:
            ax.set_title(f"Initial state - Source: {source}")
        else:
            # Find the node that was just visited
            prev_visited = states[frame-1][2]
            curr_visited = visited
            just_visited = list(curr_visited - prev_visited)
            
            if just_visited:
                ax.set_title(f"Visited node: {just_visited[0]}")
            else:
                ax.set_title(f"Step {frame}")
    
    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(states), interval=1000, repeat=True)
    
    plt.tight_layout()
    plt.close()  # This prevents the figure from being displayed directly
    
    return ani

# Create the sample graph
G = create_sample_graph()

# Create animations
floyd_ani = animate_floyd_warshall(G)
dijkstra_ani = animate_dijkstra(G, source=0)

# Save animations as GIFs
floyd_ani.save("floyd_warshall_animation.gif", writer="pillow", fps=1)
print("Floyd-Warshall animation saved as floyd_warshall_animation.gif")
plt.show()

dijkstra_ani.save("dijkstra_animation.gif", writer="pillow", fps=1)
print("Dijkstra animation saved as dijkstra_animation.gif")
plt.show()

# Display basic information about the animations
print("\nAnimations created:")
print("1. Floyd-Warshall algorithm animation - Shows the algorithm building the all-pairs shortest path matrix")
print("2. Dijkstra's algorithm animation - Shows the algorithm finding shortest paths from a source node")
print("\nThe animations show:")
print("- Floyd-Warshall: Computes shortest paths between all pairs of nodes")
print("- Dijkstra: Computes shortest paths from a single source node to all other nodes")
print("\nColor coding:")
print("- Floyd-Warshall: Red node indicates the current intermediate node k")
print("- Dijkstra: Green = source node, Red = visited nodes, Red edges = shortest path tree")