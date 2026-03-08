import math


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def optimize_travel(stitch_sequences):

    if not stitch_sequences:
        return stitch_sequences

    optimized = []
    remaining = stitch_sequences[:]

    current = remaining.pop(0)
    optimized.append(current)

    while remaining:

        last = current.stitches[-1]

        nearest = min(
            remaining,
            key=lambda seq: distance(last, seq.stitches[0])
        )

        remaining.remove(nearest)
        optimized.append(nearest)

        current = nearest

    return optimized