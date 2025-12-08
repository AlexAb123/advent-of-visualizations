from math import dist, prod
from itertools import combinations
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np
from advent_of_visualizations.utils import get_cmap, get_color
from pathlib import Path
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from math import log2, log10

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection='3d')

cmap = get_cmap("viridis")

data = (Path(__file__).parent/"inputs"/"day08.txt").read_text().strip()
points = list(map(lambda line: tuple(map(int, line.split(","))), data.split("\n")))

xs = [p[0] for p in points]
ys = [p[1] for p in points]
zs = [p[2] for p in points]
z_norm = [(z - min(zs)) / (max(zs) - min(zs)) for z in zs]
colors = [cmap(t) for t in z_norm]

connections = sorted(combinations(points, 2), key=lambda p: dist(*p))

parent = {}
size = {} # Call using size(find(x))

def find(x):
    if x not in parent: # If it's a new node, set its root to itself and it's size to 1
        parent[x] = x
        size[x] = 1
    if parent[x] != x: # If it's not its own root, set its parent to the root of its parent
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    rootx, rooty, = find(x), find(y)
    if rootx != rooty: # If they are in different sets, union them and add their sizes
        parent[rooty] = rootx
        size[rootx] += size.pop(rooty)
        return True
    return False

states = []
circuits = []
num_circuits = len(points)
for i, (p1, p2) in enumerate(connections):
    states.append([size[find(p)] for p in points])
    if union(p1, p2):
        num_circuits -= 1
    circuits.append(num_circuits)

    if size[find(p1)] >= len(points):
        break
# Set axis limits upfront
text = fig.text(0.02, 0.98, "", fontsize=16, verticalalignment='top', color="#FFFFFF")
line_collections = Line3DCollection([], linewidths=2, linestyle="-", alpha=0.4)
ax.add_collection(line_collections)
scatter = ax.scatter(xs, ys, zs, c=colors, s=15, alpha=0.8)

bg_color = "#000000"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.xaxis.pane.set_facecolor(bg_color)
ax.yaxis.pane.set_facecolor(bg_color)
ax.zaxis.pane.set_facecolor(bg_color)
ax.set_axis_off()

def size_to_color(size):
    t = ((size) / (len(points))) ** 4
    return cmap(t)

precomputed_colors = [[size_to_color(s) for s in state] for state in states]

def update(frame: int):
    ax.view_init(elev=20, azim=-(frame / 2))
    text.set_text(f"Connections: {frame}\nCircuits: {circuits[frame]}")
    line_colors = []
    line_widths = []

    for i in range(frame):
        if i == frame - 1:
            line_colors.append("#7bff00")
            line_widths.append(3)
        else:
            line_colors.append("#A10000")
            line_widths.append(1)
            
    scatter.set_color(precomputed_colors[frame])

    line_collections.set_colors(line_colors)
    line_collections.set_linewidth(line_widths)
    line_collections.set_segments([[p1, p2] for p1, p2 in connections[:frame]])


ani = FuncAnimation(fig, update, frames=len(states), interval=25)
print("Saving")
#ani.save(Path("docs") / "visualizations" / "2025" / "day08.gif", writer='pillow', fps=30)
plt.show()