from math import dist
from itertools import combinations
from pathlib import Path
import plotly.graph_objects as go
import numpy as np

# Load data
data = (Path(__file__).parent / "inputs" / "day08.txt").read_text().strip()
points = list(map(lambda line: tuple(map(int, line.split(","))), data.split("\n")))

xs = [p[0] for p in points]
ys = [p[1] for p in points]
zs = [p[2] for p in points]

connections = sorted(combinations(points, 2), key=lambda p: dist(*p))

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
for i, (p1, p2) in enumerate(connections):
    states.append([size[find(p)] for p in points])
    if union(p1, p2):
        num_circuits -= 1
    circuits.append(num_circuits)
    if size[find(p1)] >= len(points):
        break

def size_to_color(s):
    t = (s / len(points)) ** 4
    # Viridis-like: dark purple -> teal -> yellow
    r = int(255 * min(1, t * 2))
    g = int(255 * t)
    b = int(255 * (1 - t))
    return f'rgb({r},{g},{b})'

# Create frames for animation
frames = []
for frame in range(1, len(states)):
    # Point colors
    point_colors = [size_to_color(s) for s in states[frame]]

    # Lines
    line_x = []
    line_y = []
    line_z = []
    for p1, p2 in connections[:frame]:
        line_x.extend([p1[0], p2[0], None])
        line_y.extend([p1[1], p2[1], None])
        line_z.extend([p1[2], p2[2], None])

    # Latest line (highlighted)
    latest_p1, latest_p2 = connections[frame - 1]

    frame_data = go.Frame(
        data=[
            # All lines (dark red)
            go.Scatter3d(
                x=line_x, y=line_y, z=line_z,
                mode='lines',
                line=dict(color='#A10000', width=2),
                hoverinfo='skip'
            ),
            # Latest line (bright green)
            go.Scatter3d(
                x=[latest_p1[0], latest_p2[0]],
                y=[latest_p1[1], latest_p2[1]],
                z=[latest_p1[2], latest_p2[2]],
                mode='lines',
                line=dict(color='#7bff00', width=5),
                hoverinfo='skip'
            ),
            # Points
            go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode='markers',
                marker=dict(size=3, color=point_colors, opacity=0.8),
                hoverinfo='skip'
            ),
        ],
        name=str(frame),
        layout=go.Layout(
            annotations=[dict(
                text=f"Connections: {frame}<br>Circuits: {circuits[frame]}",
                x=0.02, y=0.98,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(color="white", size=14),
                align="left"
            )]
        )
    )
    frames.append(frame_data)

# Initial figure
initial_colors = [size_to_color(s) for s in states[0]]
fig = go.Figure(
    data=[
        go.Scatter3d(x=[], y=[], z=[], mode='lines', line=dict(color='#A10000', width=2)),
        go.Scatter3d(x=[], y=[], z=[], mode='lines', line=dict(color='#7bff00', width=5)),
        go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='markers',
            marker=dict(size=3, color=initial_colors, opacity=0.8)
        ),
    ],
    frames=frames
)

# Layout
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor='black',
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    showlegend=False,
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        y=0.1,
        x=0.1,
        buttons=[
            dict(label="Play",
                 method="animate",
                 args=[None, dict(frame=dict(duration=30, redraw=True),
                                  fromcurrent=True,
                                  mode='immediate')])
        ]
    )],
    sliders=[dict(
        steps=[dict(method='animate', args=[[str(k)], dict(mode='immediate', frame=dict(duration=30, redraw=True))], label=str(k))
               for k in range(1, len(states))],
        active=0,
        transition=dict(duration=0),
        x=0.1, y=0,
        len=0.8
    )],
    annotations=[dict(
        text=f"Connections: 0<br>Circuits: {circuits[0]}",
        x=0.02, y=0.98,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(color="white", size=14),
        align="left"
    )]
)

print("Saving...")
# Save as HTML for GitHub Pages
output_path = Path("docs") / "visualizations" / "2025" / "day08.html"
output_path.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(str(output_path), include_plotlyjs=True, full_html=True)
print(f"Saved to {output_path}")

