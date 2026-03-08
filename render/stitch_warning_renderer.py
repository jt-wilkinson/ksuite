from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt


def draw_long_stitches(scene, stitches):

    pen = QPen(Qt.red)
    pen.setWidth(2)

    for s1, s2 in stitches:

        line = QGraphicsLineItem(
            s1.x,
            s1.y,
            s2.x,
            s2.y
        )

        line.setPen(pen)

        scene.addItem(line)