def solve(input_path):
    lines = input_path.open("r").read().strip().split("\n")

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

    part1 = len(q)
    seen = set(q)
    while q:
        r, c = q.pop(0)
        for adj in get_adjs(r, c, lines):
            if adj in seen:
                continue
            adjs_count[adj] -= 1
            if adjs_count[adj] < 4:
                q.append(adj)
                seen.add(adj)
    part2 = len(seen)

    return part1, part2


if __name__ == "__main__":
    from pathlib import Path
    from time import time
    start = time()
    part1, part2 = solve(Path(__file__).parent / "inputs" / "day04.txt")
    print(f"Part 1: {part1}\nPart 2: {part2}")
    print(f"Time Taken: {(time() - start) * 1000:.2f} ms")
