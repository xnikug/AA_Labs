import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time
import tracemalloc
import pandas as pd
import numpy as np
from networkx.algorithms.tree import minimum_spanning_tree
import os

# Create output directory for plots
os.makedirs('mst_plots', exist_ok=True)

def generate_sparse_graph(n):
    return nx.gnm_random_graph(n, n-1, seed=random.randint(1, 100))

def generate_dense_graph(n):
    return nx.gnm_random_graph(n, n*(n-1)//2, seed=random.randint(1, 100))

def generate_grid_graph(n):
    side = int(n**0.5)
    G = nx.grid_2d_graph(side, side)
    G = nx.convert_node_labels_to_integers(G)
    return G

def generate_cycle_graph(n):
    return nx.cycle_graph(n)

def generate_star_graph(n):
    return nx.star_graph(n-1)

def generate_complete_graph(n):
    return nx.complete_graph(n)

def assign_random_weights(G):
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)
    return G

def measure_mst_performance(G, algorithm):
    tracemalloc.start()
    start_time = time.perf_counter()
    if algorithm == 'prim':
        mst = minimum_spanning_tree(G, algorithm='prim')
    elif algorithm == 'kruskal':
        mst = minimum_spanning_tree(G, algorithm='kruskal')
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return (end_time - start_time), peak / 1024  # Return time and memory in KB

def plot_graph(G, title, ax):
    pos = nx.spring_layout(G, seed=random.randint(1, 100))
    weights = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, ax=ax)
    ax.set_title(title)

def create_heatmaps(df):
    """Create heatmaps for time and memory comparison"""
    
    # Prepare data for heatmaps
    graph_types = df['Graph Type'].unique()
    sizes = sorted(df['Size'].unique())
    
    # Time ratio heatmap (Kruskal/Prim)
    time_ratio_data = np.zeros((len(graph_types), len(sizes)))
    memory_ratio_data = np.zeros((len(graph_types), len(sizes)))
    
    for i, graph_type in enumerate(graph_types):
        for j, size in enumerate(sizes):
            row = df[(df['Graph Type'] == graph_type) & (df['Size'] == size)]
            if not row.empty:
                time_ratio = row['Kruskal Time (s)'].iloc[0] / row['Prim Time (s)'].iloc[0]
                memory_ratio = row['Kruskal Memory (KB)'].iloc[0] / row['Prim Memory (KB)'].iloc[0]
                time_ratio_data[i, j] = time_ratio
                memory_ratio_data[i, j] = memory_ratio
    
    # Create time ratio heatmap
    plt.figure(figsize=(12, 8))
    mask = time_ratio_data == 0
    sns.heatmap(time_ratio_data, 
                xticklabels=sizes, 
                yticklabels=graph_types,
                annot=True, 
                fmt='.3f', 
                cmap='RdYlBu_r',
                center=1.0,
                mask=mask,
                cbar_kws={'label': 'Kruskal Time / Prim Time'})
    plt.title('Time Performance Ratio: Kruskal vs Prim\n(Values < 1.0 indicate Kruskal is faster)')
    plt.xlabel('Graph Size')
    plt.ylabel('Graph Type')
    plt.tight_layout()
    plt.savefig('mst_plots/time_ratio_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create memory ratio heatmap
    plt.figure(figsize=(12, 8))
    mask = memory_ratio_data == 0
    sns.heatmap(memory_ratio_data, 
                xticklabels=sizes, 
                yticklabels=graph_types,
                annot=True, 
                fmt='.3f', 
                cmap='RdYlBu_r',
                center=1.0,
                mask=mask,
                cbar_kws={'label': 'Kruskal Memory / Prim Memory'})
    plt.title('Memory Usage Ratio: Kruskal vs Prim\n(Values < 1.0 indicate Kruskal uses less memory)')
    plt.xlabel('Graph Size')
    plt.ylabel('Graph Type')
    plt.tight_layout()
    plt.savefig('mst_plots/memory_ratio_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create absolute performance heatmaps
    # Time heatmaps
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    prim_time_data = np.zeros((len(graph_types), len(sizes)))
    kruskal_time_data = np.zeros((len(graph_types), len(sizes)))
    
    for i, graph_type in enumerate(graph_types):
        for j, size in enumerate(sizes):
            row = df[(df['Graph Type'] == graph_type) & (df['Size'] == size)]
            if not row.empty:
                prim_time_data[i, j] = row['Prim Time (s)'].iloc[0]
                kruskal_time_data[i, j] = row['Kruskal Time (s)'].iloc[0]
    
    # Prim time heatmap
    mask = prim_time_data == 0
    sns.heatmap(prim_time_data, 
                xticklabels=sizes, 
                yticklabels=graph_types,
                annot=True, 
                fmt='.4f', 
                cmap='YlOrRd',
                mask=mask,
                ax=ax1,
                cbar_kws={'label': 'Time (seconds)'})
    ax1.set_title('Prim Algorithm - Execution Time')
    ax1.set_xlabel('Graph Size')
    ax1.set_ylabel('Graph Type')
    
    # Kruskal time heatmap
    mask = kruskal_time_data == 0
    sns.heatmap(kruskal_time_data, 
                xticklabels=sizes, 
                yticklabels=graph_types,
                annot=True, 
                fmt='.4f', 
                cmap='YlOrRd',
                mask=mask,
                ax=ax2,
                cbar_kws={'label': 'Time (seconds)'})
    ax2.set_title('Kruskal Algorithm - Execution Time')
    ax2.set_xlabel('Graph Size')
    ax2.set_ylabel('Graph Type')
    
    plt.tight_layout()
    plt.savefig('mst_plots/absolute_time_heatmaps.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    graph_types = {
        'Sparse': generate_sparse_graph,
        'Dense': generate_dense_graph,
        'Grid': generate_grid_graph,
        'Cycle': generate_cycle_graph,
        'Star': generate_star_graph,
        'Complete': generate_complete_graph,
    }

    sizes = [50, 100, 200, 300, 400, 500]

    results = []

    print("Running performance analysis...")
    for size in sizes:
        print(f"Processing size {size}...")
        for graph_name, graph_func in graph_types.items():
            G = graph_func(size)
            G = assign_random_weights(G)
            t_prim, m_prim = measure_mst_performance(G, 'prim')
            t_kruskal, m_kruskal = measure_mst_performance(G, 'kruskal')
            results.append({
                'Graph Type': graph_name,
                'Size': size,
                'Prim Time (s)': t_prim,
                'Prim Memory (KB)': m_prim,
                'Kruskal Time (s)': t_kruskal,
                'Kruskal Memory (KB)': m_kruskal
            })

    df = pd.DataFrame(results)
    
    # Save results to CSV
    df.to_csv('mst_plots/performance_results.csv', index=False)
    print("Results saved to mst_plots/performance_results.csv")

    # Create individual comparison plots for each graph type
    print("\nGenerating individual comparison plots...")
    for graph_type in df['Graph Type'].unique():
        subdf = df[df['Graph Type'] == graph_type]
        
        # Time comparison plot
        plt.figure(figsize=(10, 5))
        plt.plot(subdf['Size'], subdf['Prim Time (s)'], label='Prim Time', marker='o')
        plt.plot(subdf['Size'], subdf['Kruskal Time (s)'], label='Kruskal Time', marker='s')
        plt.title(f'Execution Time Comparison - {graph_type}')
        plt.xlabel('Graph Size')
        plt.ylabel('Time (s)')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')  # Log scale for better visualization
        plt.savefig(f'mst_plots/time_comparison_{graph_type.lower()}.png', dpi=300, bbox_inches='tight')
        plt.close()

        # Memory comparison plot
        plt.figure(figsize=(10, 5))
        plt.plot(subdf['Size'], subdf['Prim Memory (KB)'], label='Prim Memory', marker='o')
        plt.plot(subdf['Size'], subdf['Kruskal Memory (KB)'], label='Kruskal Memory', marker='s')
        plt.title(f'Memory Usage Comparison - {graph_type}')
        plt.xlabel('Graph Size')
        plt.ylabel('Memory (KB)')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')  # Log scale for better visualization
        plt.savefig(f'mst_plots/memory_comparison_{graph_type.lower()}.png', dpi=300, bbox_inches='tight')
        plt.close()


    # Create graph visualization samples
    print("\nGenerating graph visualizations...")
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))
    axes = axes.flatten()

    for idx, (graph_name, graph_func) in enumerate(graph_types.items()):
        G = graph_func(10)
        G = assign_random_weights(G)
        plot_graph(G, graph_name, axes[idx])

    plt.tight_layout()
    plt.savefig('mst_plots/graph_types_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Create heatmaps
    print("\nGenerating heatmaps...")
    create_heatmaps(df)
    
    # Create summary comparison chart
    print("\nGenerating summary comparison...")
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Overall time comparison
    for graph_type in df['Graph Type'].unique():
        subdf = df[df['Graph Type'] == graph_type]
        ax1.plot(subdf['Size'], subdf['Prim Time (s)'], label=f'{graph_type} (Prim)', linestyle='-', alpha=0.7)
        ax2.plot(subdf['Size'], subdf['Kruskal Time (s)'], label=f'{graph_type} (Kruskal)', linestyle='--', alpha=0.7)
    
    ax1.set_title('Prim Algorithm - Time Performance')
    ax1.set_xlabel('Graph Size')
    ax1.set_ylabel('Time (s)')
    ax1.set_yscale('log')
    ax1.legend()
    ax1.grid(True)
    
    ax2.set_title('Kruskal Algorithm - Time Performance')
    ax2.set_xlabel('Graph Size')
    ax2.set_ylabel('Time (s)')
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True)
    
    # Overall memory comparison
    for graph_type in df['Graph Type'].unique():
        subdf = df[df['Graph Type'] == graph_type]
        ax3.plot(subdf['Size'], subdf['Prim Memory (KB)'], label=f'{graph_type} (Prim)', linestyle='-', alpha=0.7)
        ax4.plot(subdf['Size'], subdf['Kruskal Memory (KB)'], label=f'{graph_type} (Kruskal)', linestyle='--', alpha=0.7)
    
    ax3.set_title('Prim Algorithm - Memory Usage')
    ax3.set_xlabel('Graph Size')
    ax3.set_ylabel('Memory (KB)')
    ax3.set_yscale('log')
    ax3.legend()
    ax3.grid(True)
    
    ax4.set_title('Kruskal Algorithm - Memory Usage')
    ax4.set_xlabel('Graph Size')
    ax4.set_ylabel('Memory (KB)')
    ax4.set_yscale('log')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('mst_plots/summary_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\nAll plots saved to 'mst_plots/' directory:")
    print("- time_ratio_heatmap.png: Ratio comparison heatmap for execution time")
    print("- memory_ratio_heatmap.png: Ratio comparison heatmap for memory usage")
    print("- absolute_time_heatmaps.png: Absolute time performance heatmaps")
    print("- Individual comparison plots for each graph type")
    print("- graph_types_visualization.png: Sample graphs of each type")
    print("- summary_comparison.png: Overall performance summary")
    print("- performance_results.csv: Raw performance data")