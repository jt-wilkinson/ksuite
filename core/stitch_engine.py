class Stitch:

    def __init__(self, x, y, command="stitch"):

        self.x = x
        self.y = y
        self.command = command


class StitchSequence:

    def __init__(self):

        self.stitches = []

    def add(self, stitch):

        self.stitches.append(stitch)

import numpy as np

def generate_running_stitches(vector_object, step=5):

    stitches = StitchSequence()

    for segment in vector_object.path:

        for t in np.linspace(0, 1, step):

            point = segment.point(t)

            x = point.real
            y = point.imag

            stitches.add(Stitch(x, y))

    return stitches