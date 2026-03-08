from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QColorDialog
)


class ThreadAssignDialog(QDialog):

    def __init__(self, barcode):

        super().__init__()

        self.setWindowTitle("Assign Thread")

        self.barcode = barcode
        self.rgb = (0, 0, 0)

        layout = QFormLayout()

        self.brand = QComboBox()
        self.brand.addItems([
            "Brothread",
            "Coats & Clark",
            "Madeira",
            "Isacord"
        ])

        self.code = QLineEdit()
        self.name = QLineEdit()

        self.color_button = QPushButton("Pick Color")
        self.color_button.clicked.connect(self.pick_color)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)

        layout.addRow("Barcode", QLineEdit(barcode))
        layout.addRow("Brand", self.brand)
        layout.addRow("Color Code", self.code)
        layout.addRow("Name", self.name)
        layout.addRow("Color", self.color_button)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def pick_color(self):

        color = QColorDialog.getColor()

        if color.isValid():
            self.rgb = (color.red(), color.green(), color.blue())

    def get_data(self):

        return {
            "brand": self.brand.currentText(),
            "code": self.code.text(),
            "name": self.name.text(),
            "rgb": self.rgb
        }