from math import dist
from itertools import combinations
from pathlib import Path
import pyvista as pv
import numpy as np

# Load data
data = (Path(__file__).parent / "inputs" / "day08.txt").read_text().strip()
points = list(map(lambda line: tuple(map(int, line.split(","))), data.split("\n")))
points_array = np.array(points)

xs = [p[0] for p in points]
ys = [p[1] for p in points]
zs = [p[2] for p in points]

connections = sorted(combinations(range(len(points)), 2), key=lambda p: dist(points[p[0]], points[p[1]]))

# Union-Find
parent = {}
size = {}

def find(x):
    if x not in parent:
        parent[x] = x
        size[x] = 1
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    rootx, rooty = find(x), find(y)
    if rootx != rooty:
        parent[rooty] = rootx
        size[rootx] += size.pop(rooty)
        return True
    return False

# Precompute states
states = []
circuits = []
num_circuits = len(points)
for i, (i1, i2) in enumerate(connections):
    states.append([size[find(j)] for j in range(len(points))])
    if union(i1, i2):
        num_circuits -= 1
    circuits.append(num_circuits)
    if size[find(i1)] >= len(points):
        break

def size_to_color(s):
    t = (s / len(points)) ** 4
    return t

# Setup plotter
plotter = pv.Plotter(off_screen=True, window_size=[800, 600])
plotter.set_background('black')

# Output path
output_path = Path("docs") / "visualizations" / "2025" / "day08.gif"
output_path.parent.mkdir(parents=True, exist_ok=True)

# Open GIF
plotter.open_gif(str(output_path), fps=30)

for frame in range(1, len(states)):
    plotter.clear()

    # Point colors based on cluster size
    scalars = np.array([size_to_color(s) for s in states[frame]])

    # Add points
    point_cloud = pv.PolyData(points_array)
    point_cloud['scalars'] = scalars
    plotter.add_mesh(point_cloud, scalars='scalars', cmap='viridis',
                     point_size=8, render_points_as_spheres=True,
                     show_scalar_bar=False)

    # Add lines (all except last in dark red)
    if frame > 1:
        lines = []
        for i1, i2 in connections[:frame-1]:
            lines.append([2, i1, i2])
        if lines:
            cells = np.hstack(lines)
            line_mesh = pv.PolyData(points_array, lines=cells)
            plotter.add_mesh(line_mesh, color='#A10000', line_width=2, opacity=0.6)

    # Latest line in bright green
    i1, i2 = connections[frame - 1]
    latest_line = pv.Line(points_array[i1], points_array[i2])
    plotter.add_mesh(latest_line, color='#7bff00', line_width=5)

    # Text
    plotter.add_text(f"Connections: {frame}\nCircuits: {circuits[frame]}",
                     position='upper_left', font_size=12, color='white')

    # Camera rotation
    azimuth = frame * 0.5
    plotter.camera_position = 'xy'
    plotter.camera.azimuth = azimuth
    plotter.camera.elevation = 20

    # Write frame
    plotter.write_frame()

    if frame % 50 == 0:
        print(f"Frame {frame}/{len(states)}")

plotter.close()
print(f"GIF saved to {output_path}")
