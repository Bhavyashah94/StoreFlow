from PyQt6.QtWidgets import QLabel, QVBoxLayout, QMenu, QGridLayout, QFrame, QWidget
from PyQt6.QtCore import Qt, pyqtSignal



class InventoryItemWidget(QFrame):
    right_clicked = pyqtSignal(object)  # Signal when right-clicked
    double_clicked = pyqtSignal(object)  # Signal when double-clicked

    def __init__(self, item_data, parent=None):
            super().__init__(parent)
            self.item_data = item_data  # Store item details
            self.setObjectName("inventoryItem")

            # Top: Item Name
            self.name_label = QLabel(item_data['name'])
            self.name_label.setStyleSheet("font-weight: bold; font-size: 16px;")

            # Bottom: Grid Layout with Two Columns
            self.details_layout = QGridLayout()

            # Left Column
            self.details_layout.addWidget(QLabel("GTIN:"), 0, 0)
            self.details_layout.addWidget(QLabel(item_data.get("gtin", "N/A")), 0, 1)

            self.details_layout.addWidget(QLabel("Stock:"), 1, 0)
            self.details_layout.addWidget(QLabel(str(item_data.get("stock", 0))), 1, 1)

            self.details_layout.addWidget(QLabel("Reorder Point:"), 2, 0)
            self.details_layout.addWidget(QLabel(str(item_data.get("reorder_point", 0))), 2, 1)

            # Right Column
            self.details_layout.addWidget(QLabel("MRP:"), 0, 2)
            self.details_layout.addWidget(QLabel(f"₹{item_data.get('mrp', 0):.2f}"), 0, 3)

            self.details_layout.addWidget(QLabel("Selling Price:"), 1, 2)
            self.details_layout.addWidget(QLabel(f"₹{item_data.get('selling_price', 0):.2f}"), 1, 3)

            self.details_layout.addWidget(QLabel("Cost Price:"), 2, 2)
            self.details_layout.addWidget(QLabel(f"₹{item_data.get('cost_price', 0):.2f}"), 2, 3)

            # Main Layout
            self.main_layout = QVBoxLayout(self)
            self.main_layout.addWidget(self.name_label)
            self.main_layout.addLayout(self.details_layout)

            self.setLayout(self.main_layout)
            self.setFixedHeight(120)  # Adjust height as needed


    def on_edit_clicked(self):
        self.right_clicked.emit(("edit", self.item_data))

    def on_delete_clicked(self):
        self.right_clicked.emit(("delete", self.item_data))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(self.mapToGlobal(event.pos()))
        elif event.button() == Qt.MouseButton.LeftButton:
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.item_data)

    def show_context_menu(self, position):
        menu = QMenu(self)
        menu.aboutToHide.connect(lambda: self.setProperty("hovered", False))
        menu.aboutToHide.connect(lambda: self.style().unpolish(self))
        menu.aboutToHide.connect(lambda: self.style().polish(self))
        self.update()  # Ensure UI refresh
        edit_action = menu.addAction("Edit Item")
        delete_action = menu.addAction("Delete Item")
        details_action = menu.addAction("View Details")

        action = menu.exec(position)

        if action == edit_action:
            self.right_clicked.emit(("edit", self.item_data))
        elif action == delete_action:
            self.right_clicked.emit(("delete", self.item_data))
        elif action == details_action:
            self.right_clicked.emit(("details", self.item_data))


