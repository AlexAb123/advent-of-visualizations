from itertools import combinations
import numpy as np
from advent_of_visualizations.utils import get_color, get_cmap, to_pattern, hex_to_rgb
from PIL import Image, ImageDraw, ImageFont

inside_pattern = to_pattern("""
##
##""",
pad_right=0,
pad_bottom=0)
inside_color = hex_to_rgb("#000000")

outside_pattern = to_pattern("""
##
##""",
pad_right=0,
pad_bottom=0)
outside_color = hex_to_rgb("#091B4F")

red_tile_pattern = to_pattern("""
##
##""",
pad_right=0,
pad_bottom=0)
red_tile_color = hex_to_rgb("#ff5050")

green_tile_pattern = to_pattern("""
##
##""",
pad_right=0,
pad_bottom=0)
green_tile_color = hex_to_rgb("#4dff67")


rectangle_pattern = to_pattern("""
##
##""",
pad_right=0,
pad_bottom=0)
invalid_rectangle_color = hex_to_rgb("#ff0000")
valid_rectangle_color  = hex_to_rgb("#009dff")

cell_size = len(inside_pattern)
frames = []
durations = []
cmap = get_cmap("rocket")    

def render_polygon(red_tiles, green_tiles):

    width = cols * cell_size
    height = rows * cell_size

    arr = np.full((height, width, 3), get_color(cmap(0.0)), dtype=np.uint8)

    for r in range(rows):
        for c in range(cols):
            if (r, c) in green_tiles:
                pattern = green_tile_pattern
                color = green_tile_color
            elif (r, c) in red_tiles:
                pattern = red_tile_pattern
                color = red_tile_color
            else:
                pattern = inside_pattern
                color = inside_color

            y, x = r * cell_size, c * cell_size
            arr[y:y+cell_size, x:x+cell_size][pattern] = color

    return Image.fromarray(arr)

def render_floodfill(background: Image.Image, outside):

    arr = np.array(background.copy())

    for r in range(rows):
        for c in range(cols):
            if (r, c) in outside:
                y, x = r * cell_size, c * cell_size
                arr[y:y+cell_size, x:x+cell_size][outside_pattern] = outside_color

    return Image.fromarray(arr)





from pathlib import Path
data = (Path(__file__).parent/"inputs"/"day09.txt").read_text().strip()
lines = list(map(lambda line: tuple(map(int, line.split(",")[::-1])), data.split("\n")))
combos = list(combinations(lines, 2))
num_points = len(lines)

def rectangle_area(r1, c1, r2, c2):
    return (abs(r1 - r2) + 1) * (abs(c1 - c2) + 1)
    
# Gives the index of a given point. Inverse of lines. Lines would be index to point
point_to_index = {p: i for i, p in enumerate(lines)}

row_pad = 1 # Add padding so we can move around the outside of the polygon
col_pad = 1
# Compress the grid by only keeping the coordinates that have red tiles
unique_rows = sorted(set(r for r, c in lines))
unique_cols = sorted(set(c for r, c in lines))
row_to_idx = {r: i for i, r in enumerate(unique_rows)}
col_to_idx = {c: i for i, c in enumerate(unique_cols)}
compressed_points = [(row_to_idx[r] + row_pad, col_to_idx[c] + col_pad) for r, c in lines]

# Stores tuples of (area, p1_index, p2_index)
rectangles = sorted([(
    rectangle_area(*p1, *p2), 
    compressed_points[point_to_index[p1]], 
    compressed_points[point_to_index[p2]]
) for p1, p2 in combos], reverse=True)

# Part 1 is the area of the largest rectangle
part1 = rectangles[0][0]

max_r = max(r for r, c in compressed_points)
max_c = max(c for r, c in compressed_points)

rows = max_r + 2 * row_pad # Padding on both bottom and top
cols = max_c + 2 * col_pad # Padding on both left and right
# Generate and store the green_tiles of the polygon
green_tiles = set()
red_tiles = set(compressed_points)
frames.append(render_polygon(red_tiles, green_tiles))
durations.append(50)

count = 0
for i in range(len(compressed_points)):
    r1, c1 = compressed_points[i]
    r2, c2 = compressed_points[(i+1)%num_points]

    # For columns (horizontal)
    step = 1 if c1 < c2 else -1
    for c in range(c1 + step, c2, step):
        green_tiles.add((r1, c))
        count += 1
        if count % 20 == 0:
            frames.append(render_polygon(red_tiles, green_tiles))
            durations.append(50)

    step = 1 if r1 < r2 else -1
    for r in range(r1 + step, r2, step):
        green_tiles.add((r, c1))
        count += 1
        if count % 20 == 0:
            frames.append(render_polygon(red_tiles, green_tiles))
            durations.append(50)
    
frames.append(render_polygon(red_tiles, green_tiles))
durations.append(50)



background = frames[-1]
# Flood fill the outside of the polygon
q = [(0, 0)] # We know 0, 0 is not inside the polygon because we added padding
outside = set(q)
# 2D array where the outside is 0 and the inside of the polygon is 1
inside = [[1 for _ in range(cols)] for _ in range(rows)]
while q:
    curr = q.pop(0)
    r, c = curr
    if len(outside) % 300 == 0:
        frames.append(render_floodfill(background, outside))
        durations.append(50)

    for dr, dc in (1, 0), (-1, 0), (0, 1), (0, -1):
        adj = (r + dr, c + dc)
        ar, ac = adj
        if not (0 <= ar < rows and 0 <= ac < cols):
            continue
        if adj in outside or adj in red_tiles or adj in green_tiles:
            continue
        q.append(adj)
        outside.add(adj)
        inside[ar][ac] = 0
frames.append(render_floodfill(background, outside))
durations.append(50)



# Generate a 2D prefix sum using the 'inside' array.
# Will use this 2D prefix sum to check if a rectangle is fully inside the polygon
prefix_sum = [[0 for _ in range(cols + 1)] for _ in range(rows + 1)]
for r in range(1, rows + 1):
    for c in range(1, cols + 1):
        prefix_sum[r][c] = inside[r-1][c-1] + prefix_sum[r-1][c] + prefix_sum[r][c-1] - prefix_sum[r-1][c-1]
        
def query_prefix_sum(r1, r2, c1, c2): # Assumes (r1, c1) is the top left and (r2, c2) is the bottom right.
    return prefix_sum[r2+1][c2+1] - prefix_sum[r2+1][c1] - prefix_sum[r1][c2+1] + prefix_sum[r1][c1]


def render_rectangle(background, p1, p2, area, outside, valid):
    arr = np.array(background.copy()).astype(np.float32)
    r1, c1 = p1
    r2, c2 = p2
    opacity = 0.5

    for r in range(min(r1, r2), max(r1, r2) + 1):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            color = valid_rectangle_color if (r, c) not in outside else invalid_rectangle_color
                
            y, x = r * cell_size, c * cell_size
            cell = arr[y:y+cell_size, x:x+cell_size]
            cell[rectangle_pattern] = cell[rectangle_pattern] * (1 - opacity) + np.array(color) * opacity
            
    img = Image.fromarray(arr.astype(np.uint8))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=20)  # or just omit font param

    draw.text((10, 10), f"Area: {area}", fill=(hex_to_rgb("#77ff55" if valid else "#ff4646e1")), font=font)
    return img

background = frames[-1]
part2 = 0
# For every rectangle, check if the number of inside tiles (using the prefix sum) is the same as the area of the rectangle
count = 0
view_rects = []
for area, (r1, c1), (r2, c2) in rectangles:
    view_rects.append((area, (r1, c1), (r2, c2)))
    if rectangle_area(r1, c1, r2, c2) == query_prefix_sum(*sorted([r1, r2]), *sorted([c1, c2])):
        part2 = area
        break

view_rects = view_rects[0:4] + view_rects[-16:]
for i in range(len(view_rects)):
    print(i, len(view_rects))
    area, (r1, c1), (r2, c2) = view_rects[i]
    valid = i == len(view_rects) - 1
    frames.append(render_rectangle(background, (r1, c1), (r2, c2), area, outside, valid))
    durations.append(800)

durations[-1] = 3200
duration = 50
frames[0].save(
    Path("docs") / "visualizations" / "2025" / "day09.gif",
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True
)