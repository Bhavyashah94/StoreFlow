from PyQt6.QtWidgets import (QLineEdit, QStyledItemDelegate, QVBoxLayout, QTableWidget,
                            QHeaderView, QTableWidgetItem, QWidget, QFrame, QHBoxLayout,
                            QLabel, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal

from database import Database

class CartTable(QWidget):
    def __init__(self, store_ui):
        super().__init__()
        self.store_ui = store_ui  # Reference to StoreFlowUI

        self.cart_items = {}

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Cart Table
        self.table = QTableWidget(0, 6)  # Extra column for row numbering
        self.table.setHorizontalHeaderLabels(["NO", "Item Name", "Quantity", "Price", "Discount", "Total"])

        # Hide vertical header
        self.table.verticalHeader().setVisible(False)

        # Column Sizing
        self.table.setColumnWidth(0, 50)  # Row number
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # "Item Name"
        for i in range(2, 6):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(i, 100)

        # Disable editing for non-editable columns
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.layout.addWidget(self.table)

        # Add first row with QLineEdit
        self.add_empty_row()

    def add_item_to_cart(self, item_data):
        """Adds item to cart or updates quantity if it already exists."""
        item_name = item_data['name']
        price = float(item_data['mrp'])

        if item_name in self.cart_items:
            # Item already exists, update quantity and total price
            row = self.cart_items[item_name]["row"]
            new_quantity = self.cart_items[item_name]["quantity"] + 1
            new_total = new_quantity * price

            # Update UI table
            self.table.item(row, 2).setText(str(new_quantity))  # Quantity
            self.table.item(row, 5).setText(f"{new_total:.2f}")  # Total price

            # Update dictionary
            self.cart_items[item_name]["quantity"] = new_quantity
            self.cart_items[item_name]["total"] = new_total

        else:
            # Add new row for new item
            row_count = self.table.rowCount()

            # If the last row has QLineEdit, remove it
            name_edit = self.table.cellWidget(row_count - 1, 1)
            if name_edit and isinstance(name_edit, QLineEdit):
                self.table.removeCellWidget(row_count - 1, 1)

            # Insert item details
            self.table.setItem(row_count - 1, 1, QTableWidgetItem(item_name))  # Name
            self.table.setItem(row_count - 1, 2, QTableWidgetItem("1"))  # Quantity
            self.table.setItem(row_count - 1, 3, QTableWidgetItem(f"{price:.2f}"))  # Price
            self.table.setItem(row_count - 1, 4, QTableWidgetItem("0"))  # Discount
            self.table.setItem(row_count - 1, 5, QTableWidgetItem(f"{price:.2f}"))  # Total price

            # Store in dictionary
            self.cart_items[item_name] = {
                "row": row_count - 1,
                "quantity": 1,
                "price": price,
                "total": price
            }

            # Add new empty row for next item entry
            self.add_empty_row()


    def update_row_numbers(self):
        """Updates the numbering in the first column after adding/removing rows."""
        for row in range(self.table.rowCount()):
            item = QTableWidgetItem(str(row + 1))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item)

    def add_empty_row(self):
        """Adds an empty row and inserts a QLineEdit in the 'Item Name' column."""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # Update row numbers
        self.update_row_numbers()

        # Add QLineEdit in the 'Item Name' column
        name_edit = QLineEdit(self)
        name_edit.setPlaceholderText("Search for an item...")
        self.table.setCellWidget(row_count, 1, name_edit)

        # Connect signal to show popup
        name_edit.textEdited.connect(lambda: self.show_add_item_popup(name_edit))

    def show_add_item_popup(self, name_edit):
        """Shows the Add Item popup when typing in the name field."""
        self.store_ui.toggle_overlay(True)  # Show overlay
        self.store_ui.overlayClicked.connect(self.close_popup)

        # Set popup position just below the top bar
        margin_top = 60  # Adjust based on top bar height
        screen_width = self.store_ui.width()
        
        self.popup = QWidget(self)

        self.popupSearchBar = QLineEdit()
        self.popupSearchBar.setText(name_edit.text())
        name_edit.clear()

        self.popupSearchBar.textChanged.connect(lambda: self.load_popup_items(self.popupSearchBar.text().strip()))

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.popup_items_container = QWidget()
        self.popup_items_layout = QVBoxLayout(self.popup_items_container)
        self.popup_items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.popup_items_container)

        popup_width = 800
        popup_height = 600
        popup_x = (screen_width - popup_width) // 2  # Center horizontally
        popup_y = margin_top  # Position below the top bar

        self.popupLayout = QVBoxLayout(self.popup)
        self.popupLayout.addWidget(self.popupSearchBar)
        self.popupLayout.addWidget(self.scroll_area)

        self.popup.setGeometry(popup_x, popup_y, popup_width, popup_height)
        self.popup.setStyleSheet("background-color: white; border-radius: 10px; color:  black;")
        
        self.popup.setParent(self.store_ui)  # Ensure it belongs to main window
        self.popup.show()
        self.popupSearchBar.setFocus()
        self.popup.raise_()  # 🔥 Ensure it's above the overlay

        self.load_popup_items(self.popupSearchBar.text().strip())

    def close_popup(self):
        """Closes the popup and hides the overlay."""
        if hasattr(self, "popup"):
            self.popup.close()
            del self.popup
            self.store_ui.toggle_overlay(False)  # Hide overlay

    def remove_selected_item(self):
        """Removes the selected row and updates numbering."""
        selected_rows = {index.row() for index in self.table.selectedIndexes()}
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
        self.update_row_numbers()

        # If table is empty, add a new QLineEdit in the first row
        if self.table.rowCount() == 0:
            self.add_empty_row()

    def load_popup_items(self, search_query=""):
        """Loads popup items into the UI with search filtering."""
        db = Database()
        items = db.get_inventory_items(search_query)
        print(items)

        # Clear existing widgets
        while self.popup_items_layout.count():
            item = self.popup_items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new items
        for item in items:
            item_widget = popupItemWidget(item)
            item_widget.double_clicked.connect(self.handle_double_click)
            self.popup_items_layout.addWidget(item_widget)

    def handle_double_click(self, item_data):
        """Handles double-click actions."""
        self.add_item_to_cart(item_data)
        self.close_popup()

    def clear_cart(self):
        """Clears all items from the cart after user confirmation."""
        if self.table.rowCount() == 0:
            QMessageBox.information(self, "Cart is Empty", "There are no items to clear.")
            return

        reply = QMessageBox.question(
            self, 
            "Clear Cart", 
            "Are you sure you want to remove all items from the cart?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Clear the table and reset cart data
            self.table.setRowCount(0)
            self.cart_items.clear()

            # Re-add an empty row for a new entry
            self.add_empty_row()


class popupItemWidget(QFrame):
    double_clicked = pyqtSignal(object) 
    def __init__(self, item_data, parent=None):
        super().__init__(parent)

        self.item_data = item_data

        self.name_label = QLabel()
        self.name_label.setText(str(item_data['name']))

        self.gtin_label = QLabel()
        self.gtin_label.setText(str(item_data.get('gtin', 'N/A')))
        self.gtin_label.setFixedWidth(200)

        self.mrp_label = QLabel()
        self.mrp_label.setText(str(item_data['mrp']))
        self.mrp_label.setFixedWidth(100)

        self.stock_label = QLabel()
        self.stock_label.setText(str(item_data['stock']))
        self.stock_label.setFixedWidth(100)
        
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.name_label, 1)
        self.mainLayout.addWidget(self.gtin_label, 0)
        self.mainLayout.addWidget(self.mrp_label, 0)
        self.mainLayout.addWidget(self.stock_label, 0)

        self.setLayout(self.mainLayout)
        self.setFixedHeight(50)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.item_data)
        



