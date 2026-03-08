from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPainterPath, QPen, QPainterPathStroker
from PySide6.QtCore import Qt


class VectorItem(QGraphicsPathItem):

    def __init__(self, qt_path, obj, main_window):

        super().__init__(qt_path)

        self.obj = obj
        self.main_window = main_window

        self.setAcceptHoverEvents(True)

        self.normal_pen = QPen(Qt.black)
        self.normal_pen.setWidth(1)

        self.hover_pen = QPen(Qt.darkGray)
        self.hover_pen.setWidth(2)

        self.selected_pen = QPen(Qt.blue)
        self.selected_pen.setWidth(2)

        self.setPen(self.normal_pen)

    # ---------- Accurate hit detection ----------

    def shape(self):

        stroker = QPainterPathStroker()
        stroker.setWidth(6)

        return stroker.createStroke(self.path())

    # ---------- Hover highlight ----------

    def hoverEnterEvent(self, event):

        if self.main_window.selected_item != self:
            self.setPen(self.hover_pen)

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):

        if self.main_window.selected_item != self:
            self.setPen(self.normal_pen)

        super().hoverLeaveEvent(event)

    # ---------- Click selection ----------

    def mousePressEvent(self, event):

        self.main_window.select_object(self.obj, self)

        super().mousePressEvent(event)

    # ---------- Style helpers ----------

    def set_selected_style(self):

        self.setPen(self.selected_pen)

    def set_normal_style(self):

        self.setPen(self.normal_pen)

def draw_vector(scene, vector_object, main_window):

    qt_path = QPainterPath()

    first = True

    for segment in vector_object.path:

        start = segment.start
        end = segment.end

        if first:
            qt_path.moveTo(start.real, start.imag)
            first = False

        qt_path.lineTo(end.real, end.imag)

    item = VectorItem(qt_path, vector_object, main_window)

    scene.addItem(item)

    return item