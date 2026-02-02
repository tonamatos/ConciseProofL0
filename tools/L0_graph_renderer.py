from itertools import product
import networkx as nx
import matplotlib.pyplot as plt
import os

# Parameters from the original paper
def c(n):
	if n==0:
		return 1
	return 2*n-1

def s_(n, c=c):
	if n==0:
		return (c(0),)
	return tuple([0]*n + [1])

def seq(length):
	if length == 0:
		return set([()])
	if length == 1:
		return set([(0,),(1,)])
	return set(product([0, 1], repeat=length))

def X_(n, c=c):
	X = set()
	for m in range(n+1):
		uniend_m = product(set(range(c(m)+1)), seq(n-m))
		X = X.union(uniend_m)
	return X

def L(n):
	return [((i,), (i+1,)) for i in range(n)]

def L_(n, c=c):
	if n == 0:
		return L(c(0))

	edges = []
	for v in L_(n-1):
		for j in range(2):
			new_edge = (v[0] + (j,), v[1] + (j,))
			edges.append(new_edge)

	edges = edges + L(c(n))
	edges.append((s_(n-1) + (0,), (0,)))
	edges.append(((c(n),) , s_(n-1) + (1,)))

	return edges

# Drawing

n = 3
G = nx.Graph()
G.add_edges_from(L_(n))

# Add nodes with different colors based on tuple size
for node in G.nodes():
	if len(node) == 1:
		G.add_node(node, color='salmon')  # Color for 2-element tuples
	else:
		G.add_node(node, color='skyblue')   # Color for tuples of other sizes

# Extract node colors for visualization
node_colors = [G.nodes[node]['color'] for node in G.nodes]

# Drawing and Saving
plt.figure(figsize=(10, 10)) # Slightly larger for detail
pos = nx.kamada_kawai_layout(G) # Often looks better for recursive/fractal math graphs

nx.draw(G, pos, 
        with_labels=True,
        node_color=node_colors, 
        node_size=50, 
        width=0.5,
        edge_color='gray')

# 1. Ensure the directory exists
output_dir = "./images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. Save the figure
# We use bbox_inches='tight' to remove white space for LaTeX
plt.savefig(os.path.join(output_dir, f"L0_{n}.png"), dpi=300, bbox_inches='tight')
print(f"Graph saved to {output_dir}/L0_{n}.png")

plt.show()