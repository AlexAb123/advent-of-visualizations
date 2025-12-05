from PIL import Image, ImageColor
from pathlib import Path

lines = (Path(__file__).parent / "inputs" / "day04.txt").open("r").read().strip().split("\n")
lines = list(map(list, lines))

import matplotlib.pyplot as plt

def lerp_color(value, min_val, max_val):
    t = (value - min_val) / (max_val - min_val)
    rgba = plt.cm.hot(t)  # or coolwarm, viridis, plasma, magma, hot
    return int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255)

frames = []
def render(current_wave):
    max_wave = 60
    frame = Image.new("RGB", (len(lines[0]), len(lines)), "#000000")
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if (r, c) in waves:
                cell_wave = waves[(r, c)]
                age = current_wave - cell_wave
                fade_duration = max_wave # frames to fully fade away
                brightness = max(0, 1 - age / fade_duration)
                t = cell_wave / max_wave
                rgba = plt.cm.hot(t)
                frame.putpixel((c, r), (
                    int(rgba[0] * 255 * 1),
                    int(rgba[1] * 255 * 1),
                    int(rgba[2] * 255 * 1)
                ))
                
         

    scale = 4
    frame = frame.resize((len(lines) * scale, len(lines[0]) * scale), Image.Resampling.NEAREST)
    frames.append(frame)

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
waves = {}
empty = set()
adjs_count = {}
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] != "@":
            empty.add((r, c))
            continue
        adjs_count[(r, c)] = len(list(get_adjs(r, c, lines)))
        if adjs_count[(r, c)] < 4:
            q.append((r, c))
seen = set(q)
wave = 0
render(wave)
while q:
    new_q = []
    while q:
        r, c = q.pop(0)
        waves[(r, c)] = wave

        lines[r][c] = "x"
        for adj in get_adjs(r, c, lines):
            if adj in seen:
                continue
            adjs_count[adj] -= 1
            if adjs_count[adj] < 4:
                new_q.append(adj)
                seen.add(adj)
    q = new_q
    wave += 1
    render(wave)

frames[0].save(
    Path("docs") / "visualizations" / "2025" / "day04.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0
)

min_wave = min(waves.values())
max_wave = max(waves.values())
print(min_wave, max_wave)
def render_heatmap():
    frame = Image.new("RGB", (len(lines[0]), len(lines)), "#000000")
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if (r, c) in empty:
                frame.putpixel((c, r), ImageColor.getrgb("#000000"))
            elif (r, c) in waves:
                frame.putpixel((c, r), lerp_color(waves[(r, c)], min_wave, max_wave))
            else:
                frame.putpixel((c, r), lerp_color(max_wave, min_wave, max_wave))

    scale = 4
    frame = frame.resize((len(lines) * scale, len(lines[0]) * scale), Image.Resampling.NEAREST)
    frame.save(
        Path("docs") / "visualizations" / "2025" / "day04.png",
    )
render_heatmap()