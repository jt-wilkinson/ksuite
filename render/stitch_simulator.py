from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt


class StitchSimulator:

    def __init__(self, scene):

        self.scene = scene
        self.timer = QTimer()

        self.stitches = []
        self.index = 0

        self.speed = 1   # milliseconds per stitch

        self.pen = QPen(Qt.darkRed)
        self.pen.setWidth(2)

        self.timer.timeout.connect(self.step)

    def start(self, stitch_sequences):

        self.scene.clear()

        self.stitches = []

        for seq in stitch_sequences:
            self.stitches.extend(seq.stitches)

        self.index = 0

        self.timer.start(self.speed)

    def step(self):

        if self.index >= len(self.stitches)-1:
            self.timer.stop()
            return

        s1 = self.stitches[self.index]
        s2 = self.stitches[self.index+1]

        line = QGraphicsLineItem(
            s1.x,
            s1.y,
            s2.x,
            s2.y
        )

        line.setPen(self.pen)

        self.scene.addItem(line)

        self.index += 1

    def set_speed(self, ms):

        self.speed = ms

        if self.timer.isActive():
            self.timer.start(self.speed)