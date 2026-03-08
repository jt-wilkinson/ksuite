import numpy as np
from core.stitch_engine import Stitch, StitchSequence


def generate_satin(vector_object, width=6, density=10):

    stitches = StitchSequence()

    for segment in vector_object.path:

        for t in np.linspace(0, 1, density):

            p = segment.point(t)

            x = p.real
            y = p.imag

            left = x - width / 2
            right = x + width / 2

            stitches.add(Stitch(left, y))
            stitches.add(Stitch(right, y))

    return stitches