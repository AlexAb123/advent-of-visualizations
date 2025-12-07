import numpy as np
def to_pattern(s, one="#", pad_right=1, pad_bottom=1):
    """Converts a string (with newlines) into a numpy boolean array with padding."""
    rows = s.strip().split("\n")
    height = len(rows)
    width = len(rows[0])
    arr = np.zeros((height + pad_bottom, width + pad_right), dtype=bool)
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            arr[r][c] = (ch == one)
    return arr