import numpy as np


def compute_density(stitch_sequences, cell_size=10):

    points = []

    for seq in stitch_sequences:
        for stitch in seq.stitches:
            points.append((stitch.x, stitch.y))

    if not points:
        return {}

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    grid = {}

    for x, y in points:

        gx = int((x - min_x) / cell_size)
        gy = int((y - min_y) / cell_size)

        key = (gx, gy)

        grid[key] = grid.get(key, 0) + 1

    return grid