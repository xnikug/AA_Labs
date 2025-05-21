import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np
from matplotlib.patches import FancyBboxPatch
import random

class MSTVisualizer:
    def __init__(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.suptitle(' ', fontsize=16, fontweight='bold')
        
    def create_graph(self, num_nodes=8, seed=42):
        """Create a random connected graph"""
        random.seed(seed)
        np.random.seed(seed)
        
        # Create a random connected graph
        G = nx.Graph()
        
        # Add nodes
        for i in range(num_nodes):
            G.add_node(i)
        
        # Create positions for nodes in a circle for better visualization
        pos = {}
        for i in range(num_nodes):
            angle = 2 * np.pi * i / num_nodes
            pos[i] = (np.cos(angle), np.sin(angle))
        
        # Add edges to make it connected and add some extra edges
        edges = []
        
        # First, create a cycle to ensure connectivity
        for i in range(num_nodes):
            next_node = (i + 1) % num_nodes
            weight = random.randint(1, 10)
            edges.append((i, next_node, weight))
        
        # Add some additional random edges
        for _ in range(num_nodes // 2):
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            if u != v and not G.has_edge(u, v):
                weight = random.randint(1, 15)
                edges.append((u, v, weight))
        
        # Add edges to graph
        for u, v, w in edges:
            G.add_edge(u, v, weight=w)
        
        return G, pos
    
    def prims_algorithm(self, G, start_node=0):
        """Prim's algorithm with step tracking"""
        steps = []
        visited = {start_node}
        mst_edges = []
        total_weight = 0
        
        # Initial step
        steps.append({
            'visited': visited.copy(),
            'mst_edges': mst_edges.copy(),
            'current_edge': None,
            'total_weight': total_weight,
            'description': f'Start with node {start_node}'
        })
        
        while len(visited) < len(G.nodes()):
            # Find minimum weight edge from visited to unvisited nodes
            min_edge = None
            min_weight = float('inf')
            
            for u in visited:
                for v in G.neighbors(u):
                    if v not in visited:
                        weight = G[u][v]['weight']
                        if weight < min_weight:
                            min_weight = weight
                            min_edge = (u, v)
            
            if min_edge:
                u, v = min_edge
                visited.add(v)
                mst_edges.append(min_edge)
                total_weight += min_weight
                
                steps.append({
                    'visited': visited.copy(),
                    'mst_edges': mst_edges.copy(),
                    'current_edge': min_edge,
                    'total_weight': total_weight,
                    'description': f'Add edge ({u}, {v}) with weight {min_weight}'
                })
        
        return steps
    
    def kruskals_algorithm(self, G):
        """Kruskal's algorithm with step tracking"""
        steps = []
        
        # Get all edges sorted by weight
        edges = [(u, v, G[u][v]['weight']) for u, v in G.edges()]
        edges.sort(key=lambda x: x[2])
        
        # Initialize Union-Find
        parent = {node: node for node in G.nodes()}
        rank = {node: 0 for node in G.nodes()}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if rank[px] < rank[py]:
                parent[px] = py
            elif rank[px] > rank[py]:
                parent[py] = px
            else:
                parent[py] = px
                rank[px] += 1
        
        mst_edges = []
        rejected_edges = []
        total_weight = 0
        
        # Initial step
        steps.append({
            'mst_edges': mst_edges.copy(),
            'rejected_edges': rejected_edges.copy(),
            'current_edge': None,
            'total_weight': total_weight,
            'description': 'Start with sorted edges'
        })
        
        for u, v, weight in edges:
            if find(u) != find(v):
                # Add edge to MST
                union(u, v)
                mst_edges.append((u, v))
                total_weight += weight
                
                steps.append({
                    'mst_edges': mst_edges.copy(),
                    'rejected_edges': rejected_edges.copy(),
                    'current_edge': (u, v),
                    'total_weight': total_weight,
                    'description': f'Add edge ({u}, {v}) with weight {weight}'
                })
            else:
                # Reject edge (creates cycle)
                rejected_edges.append((u, v))
                steps.append({
                    'mst_edges': mst_edges.copy(),
                    'rejected_edges': rejected_edges.copy(),
                    'current_edge': (u, v),
                    'total_weight': total_weight,
                    'description': f'Reject edge ({u}, {v}) - creates cycle'
                })
        
        return steps
    
    def animate_prim(self, frame, G, pos, steps):
        """Animation function for Prim's algorithm"""
        self.ax1.clear()
        self.ax1.set_title("Prim's Algorithm", fontsize=14, fontweight='bold')
        self.ax1.set_aspect('equal')
        
        if frame >= len(steps):
            frame = len(steps) - 1
        
        step = steps[frame]
        
        # Draw all edges in light gray
        for u, v in G.edges():
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            self.ax1.plot(x_coords, y_coords, 'lightgray', linewidth=1, zorder=1)
            
            # Draw edge weights
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            weight = G[u][v]['weight']
            self.ax1.text(mid_x, mid_y, str(weight), fontsize=8, 
                         bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8),
                         ha='center', va='center', zorder=3)
        
        # Draw MST edges in green
        for u, v in step['mst_edges']:
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            self.ax1.plot(x_coords, y_coords, 'green', linewidth=3, zorder=2)
        
        # Highlight current edge in red
        if step['current_edge']:
            u, v = step['current_edge']
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            self.ax1.plot(x_coords, y_coords, 'red', linewidth=4, zorder=4)
        
        # Draw nodes
        for node in G.nodes():
            if node in step['visited']:
                self.ax1.scatter(pos[node][0], pos[node][1], c='lightgreen', 
                               s=500, zorder=5, edgecolors='green', linewidth=2)
            else:
                self.ax1.scatter(pos[node][0], pos[node][1], c='lightblue', 
                               s=500, zorder=5, edgecolors='blue', linewidth=2)
            
            # Draw node labels
            self.ax1.text(pos[node][0], pos[node][1], str(node), 
                         fontsize=12, fontweight='bold', ha='center', va='center', zorder=6)
        
        # Add step information
        info_text = f"Step {frame + 1}/{len(steps)}\n{step['description']}\nTotal Weight: {step['total_weight']}"
        self.ax1.text(0.02, 0.98, info_text, transform=self.ax1.transAxes, 
                     verticalalignment='top', fontsize=10,
                     bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.7))
        
        self.ax1.set_xlim(-1.5, 1.5)
        self.ax1.set_ylim(-1.5, 1.5)
        self.ax1.axis('off')
    
    def animate_kruskal(self, frame, G, pos, steps):
        """Animation function for Kruskal's algorithm"""
        self.ax2.clear()
        self.ax2.set_title("Kruskal's Algorithm", fontsize=14, fontweight='bold')
        self.ax2.set_aspect('equal')
        
        if frame >= len(steps):
            frame = len(steps) - 1
        
        step = steps[frame]
        
        # Draw all edges in light gray
        for u, v in G.edges():
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            self.ax2.plot(x_coords, y_coords, 'lightgray', linewidth=1, zorder=1)
            
            # Draw edge weights
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            weight = G[u][v]['weight']
            self.ax2.text(mid_x, mid_y, str(weight), fontsize=8, 
                         bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8),
                         ha='center', va='center', zorder=3)
        
        # Draw MST edges in green
        for u, v in step['mst_edges']:
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            self.ax2.plot(x_coords, y_coords, 'green', linewidth=3, zorder=2)
        
        # Draw rejected edges in red
        for u, v in step['rejected_edges']:
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            self.ax2.plot(x_coords, y_coords, 'red', linewidth=2, alpha=0.6, 
                         linestyle='--', zorder=2)
        
        # Highlight current edge
        if step['current_edge']:
            u, v = step['current_edge']
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            if (u, v) in step['mst_edges'] or (v, u) in step['mst_edges']:
                self.ax2.plot(x_coords, y_coords, 'darkgreen', linewidth=5, zorder=4)
            else:
                self.ax2.plot(x_coords, y_coords, 'darkred', linewidth=4, zorder=4)
        
        # Draw all nodes
        for node in G.nodes():
            self.ax2.scatter(pos[node][0], pos[node][1], c='lightblue', 
                           s=500, zorder=5, edgecolors='blue', linewidth=2)
            
            # Draw node labels
            self.ax2.text(pos[node][0], pos[node][1], str(node), 
                         fontsize=12, fontweight='bold', ha='center', va='center', zorder=6)
        
        # Add step information
        info_text = f"Step {frame + 1}/{len(steps)}\n{step['description']}\nTotal Weight: {step['total_weight']}"
        self.ax2.text(0.02, 0.98, info_text, transform=self.ax2.transAxes, 
                     verticalalignment='top', fontsize=10,
                     bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.7))
        
        self.ax2.set_xlim(-1.5, 1.5)
        self.ax2.set_ylim(-1.5, 1.5)
        self.ax2.axis('off')
    
    def create_visualization(self):
        """Create and save the visualization as GIF"""
        # Create graph
        G, pos = self.create_graph()
        
        # Get algorithm steps
        prim_steps = self.prims_algorithm(G)
        kruskal_steps = self.kruskals_algorithm(G)
        
        # Make both animations the same length
        max_steps = max(len(prim_steps), len(kruskal_steps))
        
        def animate_frame(frame):
            # Clear both subplots
            self.animate_prim(frame, G, pos, prim_steps)
            self.animate_kruskal(frame, G, pos, kruskal_steps)
        
        # Create animation
        anim = animation.FuncAnimation(
            self.fig, animate_frame, frames=max_steps,
            interval=2000, repeat=True, blit=False
        )
        
        # Save as GIF
        print("Saving combined MST algorithms visualization as GIF...")
        anim.save('mst_algorithms_comparison.gif', writer='pillow', fps=0.5, dpi=100)
        print("✓ Saved: mst_algorithms_comparison.gif")
        
        plt.tight_layout()
        plt.show()
        
        return anim

# Create separate visualizations for each algorithm
def create_individual_visualizations():
    """Create individual GIFs for Prim's and Kruskal's algorithms"""
    
    # Prim's Algorithm Visualization
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    fig1.suptitle("Prim's Algorithm - Minimum Spanning Tree", fontsize=16, fontweight='bold')
    
    visualizer = MSTVisualizer()
    G, pos = visualizer.create_graph()
    prim_steps = visualizer.prims_algorithm(G)
    
    def animate_prim_only(frame):
        ax1.clear()
        ax1.set_title("Prim's Algorithm", fontsize=14, fontweight='bold')
        ax1.set_aspect('equal')
        
        if frame >= len(prim_steps):
            frame = len(prim_steps) - 1
        
        step = prim_steps[frame]
        
        # Draw all edges in light gray
        for u, v in G.edges():
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            ax1.plot(x_coords, y_coords, 'lightgray', linewidth=1, zorder=1)
            
            # Draw edge weights
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            weight = G[u][v]['weight']
            ax1.text(mid_x, mid_y, str(weight), fontsize=10, 
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8),
                    ha='center', va='center', zorder=3)
        
        # Draw MST edges in green
        for u, v in step['mst_edges']:
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            ax1.plot(x_coords, y_coords, 'green', linewidth=4, zorder=2)
        
        # Highlight current edge in red
        if step['current_edge']:
            u, v = step['current_edge']
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            ax1.plot(x_coords, y_coords, 'red', linewidth=5, zorder=4)
        
        # Draw nodes
        for node in G.nodes():
            if node in step['visited']:
                ax1.scatter(pos[node][0], pos[node][1], c='lightgreen', 
                          s=600, zorder=5, edgecolors='green', linewidth=3)
            else:
                ax1.scatter(pos[node][0], pos[node][1], c='lightblue', 
                          s=600, zorder=5, edgecolors='blue', linewidth=3)
            
            # Draw node labels
            ax1.text(pos[node][0], pos[node][1], str(node), 
                    fontsize=14, fontweight='bold', ha='center', va='center', zorder=6)
        
        # Add step information
        info_text = f"Step {frame + 1}/{len(prim_steps)}\n{step['description']}\nTotal Weight: {step['total_weight']}"
        ax1.text(0.02, 0.98, info_text, transform=ax1.transAxes, 
                verticalalignment='top', fontsize=12,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.8))
        
        ax1.set_xlim(-1.5, 1.5)
        ax1.set_ylim(-1.5, 1.5)
        ax1.axis('off')
    
    # Kruskal's Algorithm Visualization
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    fig2.suptitle("Kruskal's Algorithm - Minimum Spanning Tree", fontsize=16, fontweight='bold')
    
    kruskal_steps = visualizer.kruskals_algorithm(G)
    
    def animate_kruskal_only(frame):
        ax2.clear()
        ax2.set_title("Kruskal's Algorithm", fontsize=14, fontweight='bold')
        ax2.set_aspect('equal')
        
        if frame >= len(kruskal_steps):
            frame = len(kruskal_steps) - 1
        
        step = kruskal_steps[frame]
        
        # Draw all edges in light gray
        for u, v in G.edges():
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            ax2.plot(x_coords, y_coords, 'lightgray', linewidth=1, zorder=1)
            
            # Draw edge weights
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            weight = G[u][v]['weight']
            ax2.text(mid_x, mid_y, str(weight), fontsize=10, 
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8),
                    ha='center', va='center', zorder=3)
        
        # Draw MST edges in green
        for u, v in step['mst_edges']:
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            ax2.plot(x_coords, y_coords, 'green', linewidth=4, zorder=2)
        
        # Draw rejected edges in red
        for u, v in step['rejected_edges']:
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            ax2.plot(x_coords, y_coords, 'red', linewidth=3, alpha=0.7, 
                    linestyle='--', zorder=2)
        
        # Highlight current edge
        if step['current_edge']:
            u, v = step['current_edge']
            x_coords = [pos[u][0], pos[v][0]]
            y_coords = [pos[u][1], pos[v][1]]
            if (u, v) in step['mst_edges'] or (v, u) in step['mst_edges']:
                ax2.plot(x_coords, y_coords, 'darkgreen', linewidth=6, zorder=4)
            else:
                ax2.plot(x_coords, y_coords, 'darkred', linewidth=5, zorder=4)
        
        # Draw all nodes
        for node in G.nodes():
            ax2.scatter(pos[node][0], pos[node][1], c='lightblue', 
                       s=600, zorder=5, edgecolors='blue', linewidth=3)
            
            # Draw node labels
            ax2.text(pos[node][0], pos[node][1], str(node), 
                    fontsize=14, fontweight='bold', ha='center', va='center', zorder=6)
        
        # Add step information
        info_text = f"Step {frame + 1}/{len(kruskal_steps)}\n{step['description']}\nTotal Weight: {step['total_weight']}"
        ax2.text(0.02, 0.98, info_text, transform=ax2.transAxes, 
                verticalalignment='top', fontsize=12,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.8))
        
        ax2.set_xlim(-1.5, 1.5)
        ax2.set_ylim(-1.5, 1.5)
        ax2.axis('off')
    
    # Create animations
    anim_prim = animation.FuncAnimation(
        fig1, animate_prim_only, frames=len(prim_steps),
        interval=2000, repeat=True, blit=False
    )
    
    anim_kruskal = animation.FuncAnimation(
        fig2, animate_kruskal_only, frames=len(kruskal_steps),
        interval=2000, repeat=True, blit=False
    )
    
    # Save individual GIFs
    print("Saving Prim's algorithm visualization as GIF...")
    anim_prim.save('prims_algorithm.gif', writer='pillow', fps=0.5, dpi=100)
    print("✓ Saved: prims_algorithm.gif")
    
    print("Saving Kruskal's algorithm visualization as GIF...")
    anim_kruskal.save('kruskals_algorithm.gif', writer='pillow', fps=0.5, dpi=100)
    print("✓ Saved: kruskals_algorithm.gif")
    
    return anim_prim, anim_kruskal

if __name__ == "__main__":
    print("Creating MST Algorithm Visualizations...")
    print("=" * 50)
    
    # Create combined visualization
    visualizer = MSTVisualizer()
    combined_anim = visualizer.create_visualization()
    
    print("\nCreating individual algorithm visualizations...")
    prim_anim, kruskal_anim = create_individual_visualizations()
    
    print("\n" + "=" * 50)
    print("All visualizations created successfully!")
    print("Files generated:")
    print("1. mst_algorithms_comparison.gif - Side-by-side comparison")
    print("2. prims_algorithm.gif - Prim's algorithm only")
    print("3. kruskals_algorithm.gif - Kruskal's algorithm only")
    print("\nEach GIF shows the step-by-step process of building the minimum spanning tree.")