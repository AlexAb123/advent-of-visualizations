from PIL import Image, ImageColor
from pathlib import Path

lines = (Path(__file__).parent / "inputs" / "day04.txt").open("r").read().strip().split("\n")
lines = list(map(list, lines))

frames = []
def render():
    frame = Image.new("RGB", (len(lines[0]), len(lines)), "#000000")
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            match lines[r][c]:
                case ".":
                    frame.putpixel((c, r), ImageColor.getrgb("#545454"))
                case "x":
                    frame.putpixel((c, r),ImageColor.getrgb("#ff5555"))
                case "@":
                    frame.putpixel((c, r),ImageColor.getrgb("#33ff00"))

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
adjs_count = {}
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] != "@":
            continue
        adjs_count[(r, c)] = len(list(get_adjs(r, c, lines)))
        if adjs_count[(r, c)] < 4:
            q.append((r, c))

seen = set(q)
render()
while q:
    new_q = []
    while q:
        r, c = q.pop(0)
        lines[r][c] = "x"
        for adj in get_adjs(r, c, lines):
            if adj in seen:
                continue
            adjs_count[adj] -= 1
            if adjs_count[adj] < 4:
                new_q.append(adj)
                seen.add(adj)
    q = new_q
    render()

frames[0].save(
    Path("docs") / "visualizations" / "2025" / "day04.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=1
)
