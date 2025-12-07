from collections import defaultdict
from PIL import Image
from pathlib import Path
import numpy as np
from time import time
from advent_of_visualizations.utils import get_cmap, get_color, to_pattern

def background(height, width, bg_color, splits_color, splits, cell_size, pattern) -> np.ndarray:
    arr = np.full((height, width, 3), bg_color, dtype=np.uint8)
    for (r, c) in splits:
        y, x = r * cell_size, c * cell_size
        arr[y:y+cell_size, x:x+cell_size][pattern] = splits_color
    return arr


from math import log10
def render(timelines, rows, lines, splits, cmap, cell_pattern, split_pattern, max_t, bg_color, splits_color):
    cell_size = len(cell_pattern)
    height = len(lines[0]) * cell_size
    width = len(lines) * cell_size
    arr = background(height, width, bg_color, splits_color, splits, cell_size, split_pattern)
    for r in range(rows):
        for c in range(len(lines[0])):
            if (r, c) not in timelines:
                continue
            if (r, c) in splits:
                continue
            t = log10(timelines[(r, c)]) / log10(max_t)
            y, x = r * cell_size, c * cell_size
            color = get_color(cmap, t)
            arr[y:y+cell_size, x:x+cell_size][cell_pattern] = color

    return Image.fromarray(arr)

data = (Path(__file__).parent / "inputs" / "day07.txt").read_text().strip()
lines = data.split("\n")
splits = set()
start = (0, 0)
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == "S":
            start = (r, c)
        elif lines[r][c] == "^":
            splits.add((r, c))

q = [start]
timelines = defaultdict(int)
timelines[start] = 1
seen = set(q)
while q:
    r, c = q.pop(0)
    if (r + 1, c) in splits:
        adjs = {(r + 1, c + 1), (r + 1, c - 1)}
    else:
        adjs = {(r + 1, c)}
    for ar, ac in adjs:
        if ar >= len(lines):
            continue
        timelines[(ar, ac)] += timelines[(r, c)]
        if (ar, ac) in seen:
            continue
        q.append((ar, ac))
        seen.add((ar, ac))

part2 = 0
for c in range(len(lines[0])):
    part2 += timelines[(len(lines) - 1, c)]
print(part2)
# Settings
pat ="""
..##..
.####.
.####.
.####.
.####.
..##.."""
cell_pattern = to_pattern(pat)


pat ="""
..##..
..##..
.####.
.####.
######
######"""
split_pattern = to_pattern(pat)


def hex_to_rgb(hex_color):
    """Convert hex color (e.g., '#FF5733' or 'FF5733') to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
splits_color = hex_to_rgb("#33B500")
bg_color = hex_to_rgb("#000000")
cmap = get_cmap("Spectral_r")

max_t = max(timelines[(len(lines) - 1, c)] for c in range(len(lines[0])))
frames = []
start = time()
for r in range(len(lines)):
    frames.append(render(timelines, r, lines, splits, cmap, cell_pattern, split_pattern, max_t, bg_color, splits_color))
print(f"Rendered in: {time() - start:.2f}s")
start = time()
for _ in range(15):
    frames.append(frames[-1])
frames[0].save(
    Path("docs") / "visualizations" / "2025" / "day07.gif",
    save_all=True,
    append_images=frames[1:],
    duration=50,
    loop=0,
    optimize=True
)
print(f"Saved in: {time() - start:.2f}s")
