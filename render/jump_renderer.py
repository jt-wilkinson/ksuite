from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt


def draw_jumps(scene, jumps):

    pen = QPen(Qt.yellow)
    pen.setWidth(2)
    pen.setStyle(Qt.DashLine)

    for s1, s2 in jumps:

        line = QGraphicsLineItem(
            s1.x,
            s1.y,
            s2.x,
            s2.y
        )

        line.setPen(pen)

        scene.addItem(line)