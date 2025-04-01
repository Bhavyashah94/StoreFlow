from PyQt6.QtWidgets import (QLabel, QVBoxLayout, QMenu, QGridLayout, QFrame, QWidget,
                            QSpinBox, QLineEdit, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal

from database import Database

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
        database = Database()
        menu = QMenu(self)
        menu.aboutToHide.connect(lambda: self.setProperty("hovered", False))
        menu.aboutToHide.connect(lambda: self.style().unpolish(self))
        menu.aboutToHide.connect(lambda: self.style().polish(self))
        self.update()  # Ensure UI refresh

        # Always allow "View Details"
        details_action = menu.addAction("View Details")

        # Check if the item exists in transactions
        has_transactions = database.has_transactions(self.item_data['name'])

        # Only add "Edit Item" if the item is NOT new
        edit_action = menu.addAction("Edit Item") if has_transactions else None

        # Only add "Delete Item" if there are NO transactions
        delete_action = menu.addAction("Delete Item") if not has_transactions else None

        # Always allow "Add Stocks"
        stocks_action = menu.addAction("Add Stocks")

        action = menu.exec(position)

        # Check action only if it was actually added
        if action and action == edit_action:
            self.right_clicked.emit(("edit", self.item_data))
        elif action and action == delete_action:
            self.right_clicked.emit(("delete", self.item_data))
        elif action and action == details_action:
            self.right_clicked.emit(("details", self.item_data))
        elif action and action == stocks_action:
            AddStockPopup(self.item_data, self).show()

class AddStockPopup(QWidget):
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Stock - {item_data['name']}")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(300, 200)
        
        self.item_data = item_data
        self.parent_widget = parent
        
        layout = QVBoxLayout()
        
        # Current stock
        current_stock = QLabel(f"Current Stock: {item_data.get('stock', 0)}")
        current_stock.setStyleSheet("font-size: 14px;")
        layout.addWidget(current_stock)
        
        # Quantity input
        layout.addWidget(QLabel("Quantity to Add:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(100)
        layout.addWidget(self.quantity_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Center the window
        self.center_on_screen()
        
        # Connections
        self.confirm_button.clicked.connect(self.confirm)
        self.cancel_button.clicked.connect(self.close)
    
    def center_on_screen(self):
        frame = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
    
    def confirm(self):
        if hasattr(self.parent_widget, 'right_clicked'):
            self.parent_widget.right_clicked.emit(("add stocks confirmed", {
                'item_data': self.item_data,
                'quantity': self.quantity_input.value(),  
            }))
        self.close()