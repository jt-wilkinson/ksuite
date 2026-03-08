from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt


def draw_stitches(scene, stitch_sequence):

    pen = QPen(Qt.red)
    pen.setWidth(1)

    stitches = stitch_sequence.stitches

    for i in range(len(stitches)-1):

        s1 = stitches[i]
        s2 = stitches[i+1]

        line = QGraphicsLineItem(
            s1.x,
            s1.y,
            s2.x,
            s2.y
        )

        line.setPen(pen)

        scene.addItem(line)