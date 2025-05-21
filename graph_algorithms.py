import time
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import pandas as pd
import seaborn as sns

# Graph generation functions
def generate_sparse_graph(n, seed=None):
    """Generate a sparse graph with approximately 2*n edges"""
    if seed is not None:
        random.seed(seed)
    
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    # Add approximately 2*n edges
    edges_to_add = min(2 * n, n * (n - 1) // 2)  # Can't add more edges than complete graph
    
    edges_added = 0
    attempts = 0
    max_attempts = 100 * edges_to_add  # Avoid infinite loops
    
    while edges_added < edges_to_add and attempts < max_attempts:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v)
            edges_added += 1
        attempts += 1
    
    return G

def generate_dense_graph(n, seed=None):
    """Generate a dense graph with approximately n*(n-1)/3 edges"""
    if seed is not None:
        random.seed(seed)
    
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    # Add approximately n*(n-1)/3 edges (1/3 of complete graph)
    edges_to_add = min(n * (n - 1) // 3, n * (n - 1) // 2)
    
    edges_added = 0
    attempts = 0
    max_attempts = 100 * edges_to_add
    
    while edges_added < edges_to_add and attempts < max_attempts:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v)
            edges_added += 1
        attempts += 1
    
    return G

def generate_grid_graph(n, seed=None):
    """Generate a grid graph with approximately n nodes"""
    side = int(n ** 0.5)  # Square root to get grid dimensions
    return nx.grid_2d_graph(side, side)

def generate_cycle_graph(n, seed=None):
    """Generate a cycle graph with n nodes"""
    return nx.cycle_graph(n)

def generate_star_graph(n, seed=None):
    """Generate a star graph with n nodes"""
    return nx.star_graph(n-1)  # n-1 leaf nodes plus 1 central node

def generate_complete_graph(n, seed=None):
    """Generate a complete graph with n nodes"""
    return nx.complete_graph(n)

# Graph traversal algorithms
def dfs(G, start):
    """Depth-First Search traversal (iterative implementation to avoid recursion limits)"""
    visited = set()
    traversal_order = []
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            traversal_order.append(node)
            
            # Get neighbors and randomize their order
            neighbors = list(G.neighbors(node))
            random.shuffle(neighbors)
            
            # Add neighbors to stack in reverse order (to maintain DFS semantics)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return traversal_order

def bfs(G, start):
    """Breadth-First Search traversal"""
    visited = set([start])
    queue = deque([start])
    traversal_order = [start]
    
    while queue:
        node = queue.popleft()
        
        neighbors = list(G.neighbors(node))
        random.shuffle(neighbors)  # Randomize neighbor order
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                traversal_order.append(neighbor)
                queue.append(neighbor)
    
    return traversal_order

# Performance measurement functions
def measure_traversal_time(G, traversal_func, start_node, num_trials=10):
    """Measure the execution time of a traversal algorithm"""
    times = []
    
    for _ in range(num_trials):
        start_time = time.time()
        traversal_func(G, start_node)
        end_time = time.time()
        times.append(end_time - start_time)
    
    return np.mean(times), np.std(times)

# Main analysis function
def analyze_graph_traversals(graph_types, node_counts, num_trials=10, seed=42):
    """Analyze DFS and BFS performance on different graph types and sizes"""
    results = []
    
    for graph_name, graph_func in graph_types.items():
        print(f"Analyzing {graph_name} graphs...")
        
        for n in node_counts:
            print(f"  Nodes: {n}")
            
            # Generate graph
            G = graph_func(n, seed=seed)
            
            # Ensure graph is connected (for meaningful traversal)
            if not nx.is_connected(G):
                largest_cc = max(nx.connected_components(G), key=len)
                G = G.subgraph(largest_cc).copy()
            
            # Choose a random start node
            start_node = random.choice(list(G.nodes()))
            
            # Measure DFS performance
            dfs_time, dfs_std = measure_traversal_time(G, dfs, start_node, num_trials)
            
            # Measure BFS performance
            bfs_time, bfs_std = measure_traversal_time(G, bfs, start_node, num_trials)
            
            # Save results
            results.append({
                'Graph Type': graph_name,
                'Nodes': n,
                'Edges': G.number_of_edges(),
                'DFS Time (s)': dfs_time,
                'DFS Std Dev': dfs_std,
                'BFS Time (s)': bfs_time,
                'BFS Std Dev': bfs_std,
                'Ratio (DFS/BFS)': dfs_time / bfs_time if bfs_time > 0 else float('inf')
            })
    
    return pd.DataFrame(results)

def visualize_graph_examples(graph_types, n=20, seed=42):
    """Generate and visualize sample graphs for each type"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (graph_name, graph_func) in enumerate(graph_types.items()):
        G = graph_func(n, seed=seed)
        
        # Ensure graph is connected
        if not nx.is_connected(G):
            largest_cc = max(nx.connected_components(G), key=len)
            G = G.subgraph(largest_cc).copy()
        
        ax = axes[i]
        
        # Different layout algorithms for different graph types
        if graph_name == 'Grid':
            pos = {node: node for node in G.nodes()}
        elif graph_name == 'Star':
            pos = nx.spring_layout(G, seed=seed)
        else:
            pos = nx.spring_layout(G, seed=seed)
        
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=500, font_size=10, width=1.5, ax=ax)
        
        ax.set_title(f"{graph_name} Graph (n={G.number_of_nodes()}, e={G.number_of_edges()})")
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('graph_examples.png')
    plt.close()

def plot_performance_comparison(results):
    """Plot performance comparison between DFS and BFS"""
    # Time comparison by graph type and size
    plt.figure(figsize=(14, 8))
    
    graph_types = results['Graph Type'].unique()
    markers = ['o', 's', '^', 'D', '*', 'p']
    
    for i, graph_type in enumerate(graph_types):
        df_subset = results[results['Graph Type'] == graph_type]
        
        plt.plot(df_subset['Nodes'], df_subset['DFS Time (s)'], 
                 marker=markers[i % len(markers)], linestyle='-', label=f"{graph_type} (DFS)")
        
        plt.plot(df_subset['Nodes'], df_subset['BFS Time (s)'], 
                 marker=markers[i % len(markers)], linestyle='--', label=f"{graph_type} (BFS)")
    
    plt.xlabel('Number of Nodes')
    plt.ylabel('Execution Time (seconds)')
    plt.title('DFS vs BFS Performance Across Graph Types')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('traversal_performance.png')
    plt.close()
    
    # Ratio comparison
    plt.figure(figsize=(14, 8))
    
    for i, graph_type in enumerate(graph_types):
        df_subset = results[results['Graph Type'] == graph_type]
        
        plt.plot(df_subset['Nodes'], df_subset['Ratio (DFS/BFS)'], 
                 marker=markers[i % len(markers)], linestyle='-', label=graph_type)
    
    plt.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Equal Performance')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Performance Ratio (DFS/BFS)')
    plt.title('DFS to BFS Performance Ratio Across Graph Types')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('performance_ratio.png')
    plt.close()
    
    # Heatmap of performance by graph type
    pivot_df = results.pivot_table(
        index='Graph Type', 
        columns='Nodes',
        values=['DFS Time (s)', 'BFS Time (s)']
    )
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    sns.heatmap(pivot_df['DFS Time (s)'], annot=True, cmap='YlOrRd', ax=ax1, fmt='.4f')
    ax1.set_title('DFS Execution Time by Graph Type and Size')
    
    sns.heatmap(pivot_df['BFS Time (s)'], annot=True, cmap='YlGnBu', ax=ax2, fmt='.4f')
    ax2.set_title('BFS Execution Time by Graph Type and Size')
    
    plt.tight_layout()
    plt.savefig('performance_heatmap.png')
    plt.close()

def run_complete_analysis():
    """Run complete analysis pipeline"""
    # Define graph types for analysis
    graph_types = {
        'Sparse': generate_sparse_graph,
        'Dense': generate_dense_graph,
        'Grid': generate_grid_graph,
        'Cycle': generate_cycle_graph,
        'Star': generate_star_graph,
        'Complete': generate_complete_graph
    }
    
    # Define node counts for analysis (reduced sizes to avoid memory issues)
    node_counts_standard = [100, 250, 500, 750, 1000]
    node_counts_intensive = [50, 100, 200, 350, 500]
    
    # Use smaller counts for dense and complete graphs which are more computationally intensive
    node_counts = {}
    for graph_type in graph_types.keys():
        if graph_type in ['Dense', 'Complete']:
            node_counts[graph_type] = node_counts_intensive
        else:
            node_counts[graph_type] = node_counts_standard
    
    # Visualize example graphs
    print("Generating graph visualizations...")
    visualize_graph_examples(graph_types)
    
    # Run analysis
    print("Running traversal analysis...")
    all_results = []
    
    for graph_name, graph_func in graph_types.items():
        results = analyze_graph_traversals(
            {graph_name: graph_func}, 
            node_counts[graph_name],
            num_trials=5
        )
        all_results.append(results)
    
    combined_results = pd.concat(all_results)
    
    # Save results to CSV
    combined_results.to_csv('traversal_results.csv', index=False)
    
    # Plot results
    print("Generating performance plots...")
    plot_performance_comparison(combined_results)
    
    # Theoretical analysis
    print("\nTheoretical Analysis:")
    print("---------------------")
    print("DFS and BFS both have a time complexity of O(V + E) where V is the number of vertices and E is the number of edges.")
    print("However, their practical performance can differ based on graph structure and implementation details.\n")
    
    # Summary of results
    print("\nEmpirical Results Summary:")
    print("-------------------------")
    for graph_type in graph_types.keys():
        type_results = combined_results[combined_results['Graph Type'] == graph_type]
        avg_ratio = type_results['Ratio (DFS/BFS)'].mean()
        
        print(f"{graph_type} Graphs: DFS is {avg_ratio:.2f}x the time of BFS on average")
    
    # Return the results for further analysis
    return combined_results

# Run the analysis
if __name__ == "__main__":
    results = run_complete_analysis()
    
    # Display key insights
    print("\nKey Insights:")
    print("-------------")
    
    best_for_dfs = results.groupby('Graph Type')['Ratio (DFS/BFS)'].mean().idxmin()
    worst_for_dfs = results.groupby('Graph Type')['Ratio (DFS/BFS)'].mean().idxmax()
    
    print(f"DFS performs best relative to BFS on {best_for_dfs} graphs")
    print(f"DFS performs worst relative to BFS on {worst_for_dfs} graphs")
    
    # Memory usage comparison
    print("\nMemory Usage:")
    print("-------------")
    print("DFS typically uses less memory than BFS because:")
    print("- DFS uses a stack (often implemented with recursion) that grows proportionally to the depth of the graph")
    print("- BFS uses a queue that can grow proportionally to the breadth of the graph")
    print("- For wide graphs (high branching factor), BFS can consume significantly more memory than DFS")
    print("- For deep graphs with limited branching, DFS may use more memory than BFS")