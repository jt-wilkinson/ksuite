import math


def detect_jumps(stitch_sequences, threshold=15):

    jumps = []

    for seq in stitch_sequences:

        stitches = seq.stitches

        for i in range(len(stitches) - 1):

            s1 = stitches[i]
            s2 = stitches[i + 1]

            dist = math.hypot(
                s2.x - s1.x,
                s2.y - s1.y
            )

            if dist > threshold:

                jumps.append((s1, s2))

    return jumps