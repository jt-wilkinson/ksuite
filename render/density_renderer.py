from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt


def draw_density(scene, density_grid, cell_size):

    for (gx, gy), count in density_grid.items():

        if count < 3:
            continue

        intensity = min(count * 20, 255)

        color = QColor(255, 0, 0, intensity)

        rect = QGraphicsRectItem(
            gx * cell_size,
            gy * cell_size,
            cell_size,
            cell_size
        )

        rect.setBrush(QBrush(color))
        rect.setPen(Qt.NoPen)

        scene.addItem(rect)