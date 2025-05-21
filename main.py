import networkx as nx
import random
import time
import tracemalloc
import matplotlib.pyplot as plt
import heapq
import pandas as pd
import os

# Create directory for figure exports if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Function to generate a sparse graph (number of edges = number of nodes - 1)
def generate_sparse_graph(n):
    return nx.gnm_random_graph(n, n-1, seed=random.randint(1, 1000))

# Function to generate a dense graph (fully connected)
def generate_dense_graph(n):
    return nx.gnm_random_graph(n, n*(n-1)//2, seed=random.randint(1, 1000))

# Implementation of Floyd-Warshall algorithm for all-pairs shortest paths
def floyd_warshall(graph):
    nodes = list(graph.keys())
    INF = float('inf')
    # Initialize distance matrix with infinity
    dist = {node: {other: INF for other in nodes} for node in nodes}

    # Set initial distances based on graph edges
    for u in graph:
        for v in graph[u]:
            dist[u][v] = graph[u][v]
        dist[u][u] = 0  # Distance to self is 0

    # Core Floyd-Warshall algorithm with triple nested loop
    for k in nodes:
        for i in nodes:
            for j in nodes:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# Implementation of Dijkstra's algorithm for single-source shortest paths
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if node already processed
        if current_node in visited:
            continue

        visited.add(current_node)

        # Process all neighbors of current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Function to measure execution time and memory usage of algorithms
def measure_algorithm_performance(graph, algorithm, start_node=None):
    tracemalloc.start()
    start_time = time.perf_counter()

    if algorithm == 'floyd_warshall':
        dist = floyd_warshall(graph)
    elif algorithm == 'dijkstra':
        dist = dijkstra(graph, start_node)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return (end_time - start_time), peak / 1024  # Time in seconds, memory in KB

if __name__ == "__main__":
    # Define graph types to test
    graph_types = {
        'Sparse': generate_sparse_graph,
        'Dense': generate_dense_graph
    }

    # Graph sizes to test
    sizes = [10, 25, 50, 100, 250]

    # Store performance results
    results = []

    # Run tests for each graph size and type
    for size in sizes:
        for graph_name, graph_func in graph_types.items():
            # Generate graph and convert to dictionary representation
            G = graph_func(size)
            # Create adjacency dictionary with random edge weights
            G = {str(i): {str(j): random.randint(1, 10) for j in range(size) if i != j} for i in range(size)}

            # Measure Floyd-Warshall performance (all-pairs)
            t_fw, m_fw = measure_algorithm_performance(G, 'floyd_warshall')

            # Measure Dijkstra performance (run for all possible source nodes)
            total_time_dijkstra = 0
            total_memory_dijkstra = 0
            for node in G:
                t_dijkstra, m_dijkstra = measure_algorithm_performance(G, 'dijkstra', start_node=node)
                total_time_dijkstra += t_dijkstra
                total_memory_dijkstra += m_dijkstra

            # Store results for this configuration
            results.append({
                'Graph Type': graph_name,
                'Size': size,
                'Floyd-Warshall Time (s)': t_fw,
                'Floyd-Warshall Memory (KB)': m_fw,
                'Dijkstra Time (s)': total_time_dijkstra,
                'Dijkstra Memory (KB)': total_memory_dijkstra
            })

    # Create DataFrame from results for easy analysis
    df = pd.DataFrame(results)
    print(df)

    # Plot results for each graph type
    for graph_type in df['Graph Type'].unique():
        subdf = df[df['Graph Type'] == graph_type]

        # Plot execution time comparison
        plt.figure(figsize=(10, 5))
        plt.plot(subdf['Size'], subdf['Floyd-Warshall Time (s)'], label='Floyd-Warshall Time')
        plt.plot(subdf['Size'], subdf['Dijkstra Time (s)'], label='Dijkstra Time')
        plt.title(f'Execution Time Comparison - {graph_type}')
        plt.xlabel('Graph Size')
        plt.ylabel('Time (s)')
        plt.legend()
        plt.grid(True)
        # Save figure as PNG
        plt.savefig(f"figures/time_comparison_{graph_type}.png", dpi=300, bbox_inches='tight')

        # Plot memory usage comparison
        plt.figure(figsize=(10, 5))
        plt.plot(subdf['Size'], subdf['Floyd-Warshall Memory (KB)'], label='Floyd-Warshall Memory')
        plt.plot(subdf['Size'], subdf['Dijkstra Memory (KB)'], label='Dijkstra Memory')
        plt.title(f'Memory Usage Comparison - {graph_type}')
        plt.xlabel('Graph Size')
        plt.ylabel('Memory (KB)')
        plt.legend()
        plt.grid(True)
        # Save figure as PNG
        plt.savefig(f"figures/memory_comparison_{graph_type}.png", dpi=300, bbox_inches='tight')


    # Visualize example sparse and dense graphs
    fig, axes = plt.subplots(1, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, (graph_name, graph_func) in enumerate(graph_types.items()):
        G = graph_func(10)
        ax = axes[idx]
        pos = nx.spring_layout(G, seed=random.randint(1, 1000))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', ax=ax)
        ax.set_title(f'{graph_name} Graph')

    plt.tight_layout()
    # Save sample graphs visualization as PNG
    plt.savefig("figures/sample_graphs.png", dpi=300, bbox_inches='tight')