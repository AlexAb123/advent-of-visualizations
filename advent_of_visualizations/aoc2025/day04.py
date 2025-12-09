from PIL import Image
from pathlib import Path
import numpy as np
from time import time
from advent_of_visualizations.utils import get_color, get_cmap

lines = (Path(__file__).parent / "inputs" / "day04.txt").open("r").read().strip().split("\n")
lines = list(map(list, lines))



def solve(data):

    lines = data.split("\n")

    def get_adjs(r, c, lines):
        for dr in -1, 0, 1:
            for dc in -1, 0, 1:
                if dr == dc == 0:
                    continue
                if not (0 <= r + dr < len(lines) and 0 <= c + dc < len(lines[0])):
                    continue
                if lines[r + dr][c + dc] != "@":
                    continue
                yield (r + dr, c + dc)

    q = []
            
    adjs_count = {}
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if lines[r][c] != "@":
                continue
            adjs_count[(r, c)] = len(list(get_adjs(r, c, lines)))
            if adjs_count[(r, c)] < 4:
                q.append((r,c))

    seen = set(q)
    waves = {}
    wave = 0
    while q:
        new_q = []
        while q:
            r, c = q.pop(0)
            waves[(r, c)] = wave
            for adj in get_adjs(r, c, lines):
                if adj in seen:
                    continue
                adjs_count[adj] -= 1
                if adjs_count[adj] < 4:
                    new_q.append(adj)
                    seen.add(adj)
        q = new_q
        wave += 1

    return lines, waves, adjs_count.keys()

pattern = np.array([
[0, 1, 1, 1, 1, 0, 0],
[1, 1, 1, 1, 1, 1, 0],
[1, 1, 1, 1, 1, 1, 0],
[1, 1, 1, 1, 1, 1, 0],
[1, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 1, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
], dtype=bool)
def render(lines, current_wave, waves, rolls, duration, cmap):
    cell_size = len(pattern)
    width = len(lines[0]) * cell_size
    height = len(lines) * cell_size

    arr = np.full((height, width, 3), get_color(cmap(0.0)), dtype=np.uint8)

    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if (r, c) in waves and waves[(r, c)] <= current_wave:
                cell_wave = waves[(r, c)]
                age = current_wave - cell_wave
                t = max(0.0, 1.0 - (age / duration))
                color = get_color(cmap(t))

            elif (r, c) in rolls:
                color = get_color(cmap(1.0))

            else:
                continue

            y, x = r * cell_size, c * cell_size
            arr[y:y+cell_size, x:x+cell_size][pattern] = color

    return Image.fromarray(arr)

data = (Path(__file__).parent/"inputs"/"day04.txt").read_text().strip()
lines, waves, rolls = solve(data)
cmap = get_cmap("rocket")
frames = []
duration = 30
start = time()
for i in range(0, max(waves.values()) + duration):
    frames.append(render(lines, i, waves, rolls, duration, cmap))
for _ in range(10):
    frames.append(frames[-1])
print(f"Rendered in: {time() - start:.2f}s")
frames[0].save(
    Path("docs") / "visualizations" / "2025" / "day04.gif",
    save_all=True,
    append_images=frames[1:],
    duration=50,
    loop=0,
    optimize=True
)