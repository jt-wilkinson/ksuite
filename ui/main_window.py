from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QListWidget,
    QFileDialog,
    QWidget,
    QFormLayout,
    QComboBox
)

from PySide6.QtCore import Qt

from core.document import KDocument
from core.svg_importer import import_svg
from render.vector_renderer import draw_vector

from .canvas_view import CanvasView

from datetime import datetime

from core.stitch_engine import generate_running_stitches
from render.stitch_renderer import draw_stitches
from core.pes_exporter import export_pes
from render.stitch_simulator import StitchSimulator
from core.density_analyzer import compute_density
from render.density_renderer import draw_density
from core.travel_optimizer import optimize_travel
from core.jump_detector import detect_jumps
from render.jump_renderer import draw_jumps
from core.stitch_analyzer import detect_long_stitches
from render.stitch_warning_renderer import draw_long_stitches
from PySide6.QtCore import QThread
from core.thread_scanner import ThreadScanner
from core.thread_db import ThreadDB
from ui.thread_dialog import ThreadAssignDialog
from PySide6.QtWidgets import QTextEdit
from core.image_importer import import_image


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("KSuite")
        self.resize(1400,900)

        self.document = KDocument()

        self.selected_object = None
        self.selected_item = None
        self.canvas_items = {}

        self.thread_db = ThreadDB()

        self.setup_ui()

    def setup_ui(self):

        self.canvas = CanvasView()

        self.setCentralWidget(self.canvas)

        self.object_list = QListWidget()

        dock = QDockWidget("Objects")
        dock.setWidget(self.object_list)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        self.object_list.currentRowChanged.connect(self.object_list_selection_changed)

        self.properties_widget = QWidget()

        self.properties_layout = QFormLayout()

        self.properties_widget.setLayout(self.properties_layout)

        self.simulator = StitchSimulator(self.canvas.scene)

        self.properties_widget = QWidget()
        self.properties_layout = QFormLayout()

        self.properties_widget.setLayout(self.properties_layout)

        prop_dock = QDockWidget("Properties")
        prop_dock.setWidget(self.properties_widget)

        self.addDockWidget(Qt.RightDockWidgetArea, prop_dock)

        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)

        console_dock = QDockWidget("Output")
        console_dock.setWidget(self.output_console)
        console_dock.setMaximumHeight(240)

        self.addDockWidget(Qt.RightDockWidgetArea, console_dock)

        self.splitDockWidget(prop_dock, console_dock, Qt.Vertical)

        self.create_menu()

    def create_menu(self):

        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        import_svg_action = file_menu.addAction("Import SVG")
        import_svg_action.triggered.connect(self.import_svg_file)

        import_img_action = file_menu.addAction("Import Image")
        import_img_action.triggered.connect(self.import_image_file)

        export_action = file_menu.addAction("Export PES")
        export_action.triggered.connect(self.export_pes_file)

        # Stitch menu
        stitch_menu = menubar.addMenu("Stitches")

        generate_action = stitch_menu.addAction("Generate Stitches")
        generate_action.triggered.connect(self.generate_stitches)

        preview_action = stitch_menu.addAction("Stitch Preview")
        preview_action.triggered.connect(self.show_stitches)

        # Analysis menu
        analysis_menu = menubar.addMenu("Analysis")

        density_action = analysis_menu.addAction("Show Density Map")
        density_action.triggered.connect(self.show_density)

        jump_action = analysis_menu.addAction("Show Jump Stitches")
        jump_action.triggered.connect(self.show_jumps)

        warn_action = analysis_menu.addAction("Show Long Stitches")
        warn_action.triggered.connect(self.show_long_stitches)

        # Tools menu
        tools_menu = menubar.addMenu("Tools")

        scan_thread_action = tools_menu.addAction("Scan Thread")
        scan_thread_action.triggered.connect(self.scan_thread)

        # Sim menu
        sim_menu = menubar.addMenu("Simulation")

        simulate_action = sim_menu.addAction("Simulate Stitching")
        simulate_action.triggered.connect(self.simulate_stitches)

    def import_svg_file(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import SVG",
            "",
            "SVG Files (*.svg)"
        )

        if not path:
            return

        self.document.clear()

        objects = import_svg(path)

        for obj in objects:

            self.document.add_object(obj)

        self.refresh_view()

    def refresh_view(self):

        self.canvas.clear()
        self.object_list.clear()

        self.canvas_items = {}

        for i, obj in enumerate(self.document.objects):

            item = draw_vector(self.canvas.scene, obj, self)

            self.canvas_items[obj] = item

            self.object_list.addItem(f"Object {i}")

        self.canvas.fitInView(self.canvas.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def generate_stitches(self):

        self.document.generate_stitches(generate_running_stitches)

        self.document.stitches = optimize_travel(self.document.stitches)

        self.log("Stitches generated and optimized")

    def show_stitches(self):

        self.canvas.clear()

        for seq in self.document.stitches:

            draw_stitches(self.canvas.scene, seq)

    def select_object(self, obj, item):

        if self.selected_item:
            self.selected_item.set_normal_style()

        self.selected_object = obj
        self.selected_item = item

        item.set_selected_style()

        index = self.document.objects.index(obj)
        self.object_list.setCurrentRow(index)

        self.update_properties_panel()
        
    def update_properties_panel(self):

        for i in reversed(range(self.properties_layout.rowCount())):
            self.properties_layout.removeRow(i)

        if not self.selected_object:
            return

        stitch_type = QComboBox()

        stitch_type.addItems([
            "running",
            "satin",
            "fill"
        ])

        stitch_type.setCurrentText(self.selected_object.stitch_type)

        stitch_type.currentTextChanged.connect(self.change_stitch_type)

        self.properties_layout.addRow("Stitch Type", stitch_type)

    def change_stitch_type(self, value):

        if not self.selected_object:
            return

        self.selected_object.stitch_type = value

        self.log("Stitch type changed:", value)

    def object_list_selection_changed(self, index):

        if index < 0 or index >= len(self.document.objects):
            return

        obj = self.document.objects[index]
        item = self.canvas_items.get(obj)

        if not item:
            return

        self.select_object(obj, item)

    def export_pes_file(self):

        if not self.document.stitches:
            self.log("No stitches to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PES",
            "",
            "PES Files (*.pes)"
        )

        if not path:
            return

        export_pes(path, self.document.stitches)

        self.log("Exported PES:", path)

    def simulate_stitches(self):

        if not self.document.stitches:
            self.log("Generate stitches first")
            return
        
        self.simulator.start(self.document.stitches)

    def show_density(self):

        if not self.document.stitches:
            return

        self.canvas.clear()

        grid = compute_density(self.document.stitches)

        draw_density(self.canvas.scene, grid, 10)

    def show_jumps(self):

        jumps = detect_jumps(self.document.stitches)

        draw_jumps(self.canvas.scene, jumps)

    def show_long_stitches(self):

        warnings = detect_long_stitches(self.document.stitches)

        draw_long_stitches(self.canvas.scene, warnings)

    def scan_thread(self):

        self.log("Starting thread scan...")

        self.thread = QThread()
        self.scanner = ThreadScanner()

        self.scanner.moveToThread(self.thread)

        self.thread.started.connect(self.scanner.run)

        self.scanner.barcode_found.connect(self.on_barcode_found)

        self.scanner.finished.connect(self.thread.quit)
        self.scanner.finished.connect(self.scanner.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_barcode_found(self, barcode):

        self.log("Barcode detected:", barcode)

        thread = self.thread_db.lookup_barcode(barcode)

        if thread:
            self.log("Thread found:", thread)
            return

        self.log("Unknown thread. Opening assignment dialog.")

        dialog = ThreadAssignDialog(barcode)

        if dialog.exec():

            data = dialog.get_data()

            self.thread_db.add_thread(
                barcode,
                data["brand"],
                data["code"],
                data["name"],
                data["rgb"]
            )

            self.log("Thread saved to database")

    def log(self, *args):

        message = " ".join(str(a) for a in args)

        timestamp = datetime.now().strftime("%H:%M:%S")

        line = f"[{timestamp}] {message}"

        print(line)

        self.output_console.append(line)

        scrollbar = self.output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def import_image_file(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Image",
            "",
            "Images (*.jpg *.jpeg *.png)"
        )

        if not path:
            return

        try:

            self.document.clear()

            objects = import_image(path, self.log)

            if not objects:
                self.log("No vectors detected.")
                return

            for obj in objects:
                self.document.add_object(obj)

            self.refresh_view()

            self.log("Image imported successfully")

        except Exception as e:

            self.log("Import failed:", str(e))