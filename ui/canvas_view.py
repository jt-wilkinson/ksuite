from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt


class CanvasView(QGraphicsView):

    def __init__(self):

        super().__init__()

        self.scene = QGraphicsScene()

        self.setScene(self.scene)

        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def clear(self):

        self.scene.clear()

    def wheelEvent(self, event):

        zoom = 1.25

        if event.angleDelta().y() > 0:
            self.scale(zoom, zoom)
        else:
            self.scale(1/zoom, 1/zoom)