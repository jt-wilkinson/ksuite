from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog


def create_menus(window):

    menubar = window.menuBar()

    file_menu = menubar.addMenu("File")

    import_svg = QAction("Import SVG", window)
    import_svg.triggered.connect(lambda: import_svg_file(window))

    export_pes = QAction("Export PES", window)

    file_menu.addAction(import_svg)
    file_menu.addAction(export_pes)


def import_svg_file(window):

    path, _ = QFileDialog.getOpenFileName(
        window,
        "Import SVG",
        "",
        "SVG Files (*.svg)"
    )

    if path:
        print("Imported:", path)