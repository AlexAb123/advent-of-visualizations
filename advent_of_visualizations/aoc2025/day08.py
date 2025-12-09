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

fig = plt.figure(figsize=(10, 8), dpi=50)
ax = fig.add_subplot(1, 1, 1, projection='3d')

cmap = get_cmap("Spectral_r")

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
connection_counts = []
num_circuits = len(points)
states.append([size[find(p)] for p in points])
circuits.append(num_circuits)
connection_counts.append(0)
skip_frames = 15
for i, (p1, p2) in enumerate(connections):
    if union(p1, p2):
        num_circuits -= 1
    if i % skip_frames == 0:
        states.append([size[find(p)] for p in points])
        circuits.append(num_circuits)
        connection_counts.append(i + 1)
    if size[find(p1)] >= len(points):
        states.append([size[find(p)] for p in points])
        circuits.append(num_circuits)
        connection_counts.append(i + 1)
        break
# Set axis limits upfront
text = fig.text(0.02, 0.98, "", fontsize=16, verticalalignment='top', color="#FFFFFF")
line_collections = Line3DCollection([], linewidths=2, linestyle="-", alpha=0.4)
ax.add_collection(line_collections)

marker_radius = 30
scatter = ax.scatter(xs, ys, zs, c=colors, s=marker_radius, alpha=0.6, depthshade=True)
ax.set_box_aspect((1, 1, 1), zoom=1.2)
bg_color = "#000000"
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.xaxis.pane.set_facecolor(bg_color)
ax.yaxis.pane.set_facecolor(bg_color)
ax.zaxis.pane.set_facecolor(bg_color)
ax.set_axis_off()

def size_to_color(size):
    x = size / len(points)
    t = x ** 0.5 * 0.8 + x ** 10 * 0.2
    return cmap(t)

def shorten_line(p1, p2):
    """Move endpoints inward by radius amount"""
    p1, p2 = np.array(p1), np.array(p2)
    direction = p2 - p1                    # Vector from p1 to p2
    length = np.linalg.norm(direction)     # Length of that vector
    unit = direction / length              # Same direction, length = 1
    new_p1 = p1 + unit * marker_radius  # Move p1 toward p2 by radius
    new_p2 = p2 - unit * marker_radius  # Move p2 toward p1 by radius
    return new_p1, new_p2

precomputed_colors = [[size_to_color(s) for s in state] for state in states]
precomputed_segments = [shorten_line(p1, p2) for p1, p2 in connections[:len(states)*skip_frames]]

precomputed_line_colors = []
precomputed_line_widths = []

for frame in range(len(states)):
    colors_f = ["#6CE621"] * frame
    widths_f = [1] * frame
   
    precomputed_line_colors.append(colors_f)
    precomputed_line_widths.append(widths_f)

def update(frame: int):
    ax.view_init(elev=25, azim=(frame / 2))
    frame = min(frame, len(states) - 1)
    text.set_text(f"Connections: {connection_counts[frame]}\nCircuits: {circuits[frame]}")
    scatter.set_color(precomputed_colors[frame])
    line_collections.set_colors(precomputed_line_colors[frame])
    line_collections.set_linewidth(precomputed_line_widths[frame])
    line_collections.set_segments(precomputed_segments[:frame*skip_frames])

print("Rendering...")
pause_frames = 50
ani = FuncAnimation(fig, update, frames=len(states) + pause_frames, interval=50)
print("Saving...")
ani.save(Path("docs") / "visualizations" / "2025" / "day08_hd.gif", writer='pillow', fps=30, dpi=100)
#plt.show()