from PyQt6.QtWidgets import (QLineEdit, QVBoxLayout, QTableWidget,
                            QHeaderView, QTableWidgetItem, QWidget, QFrame, QHBoxLayout,
                            QLabel, QScrollArea, QMessageBox, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal

from database import Database

class CartTable(QWidget):
    def __init__(self, store_ui, parent):
        super().__init__()
        self.store_ui = store_ui  # Reference to StoreFlowUI

        self.parent = parent

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
            self.parent.update_summary()

        else:
            # Add new row for new item
            row_count = self.table.rowCount()

            self.table.cellDoubleClicked.connect(self.cart_item_manipulation)

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
                "discount": 0,  # Default discount
                "total": price  # Update total if discount changes
            }


            # Add new empty row for next item entry
            self.add_empty_row()
            self.parent.update_summary()

    def remove_item_from_cart(self, row):
        name = self.table.item(row,1).text()
        reply = QMessageBox.question(
            self, 
            "Remove Item", 
            f"Are you sure you want to remove {name} from the cart?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            self.cart_items.pop(name)
            self.close_item_manipulation_popup()
            self.update_row_numbers()
            self.parent.update_summary()
        else:
            return

    def cart_item_manipulation(self, row, column):

        self.store_ui.toggle_overlay(True)  # Show overlay
        self.store_ui.overlayClicked.connect(self.close_item_manipulation_popup)

        if row >= 0 and row != self.table.rowCount()-1:
            item_name = self.table.item(row, 1).text()
            quantity = self.table.item(row, 2).text()
            rate = self.table.item(row, 3).text()
            discount = self.table.item(row, 4).text()
            total = self.table.item(row, 5).text()
        else:
            return

        item_data = {
            "name" : item_name,
            "quantity" : quantity,
            "price" : rate,
            "discount" : discount,
            "total" : total
        }
        
        self.item_manipulation_popup = QWidget(self)
        # Title Bar
        self.title_bar = QFrame(self)
        self.title_bar.setStyleSheet("background-color: #444; color: white; padding: 5px;")
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(10, 0, 10, 0)

        self.title_label = QLabel("Edit Cart Item")
        self.title_label.setStyleSheet("color: white;")
        self.close_button = QPushButton("✖")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("background: none; color: white; border: none;")
        self.close_button.clicked.connect(self.close_item_manipulation_popup)

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button)
        self.title_bar.setFixedHeight(50)
    
        name_label = QLabel(f"Item Name: {item_name}")
        name_label.setFixedHeight(60)
        name_label.setContentsMargins(10, 10, 10, 10)
        
        grid_layout = QGridLayout()
        
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(10)
        
        quantity_input = QLineEdit(quantity)
        quantity_input.setPlaceholderText("Enter Quantity.")

        rate = QLineEdit(rate)
        rate.setPlaceholderText("Enter Rate.")
        
        discount1 = QLineEdit(discount)
        discount1.setPlaceholderText("Enter Discount.")

        grid_layout.addWidget(QLabel("Quantity: "), 0, 0)
        grid_layout.addWidget(quantity_input, 0, 1)
        
        grid_layout.addWidget(QLabel("Rate: "), 1, 0)
        grid_layout.addWidget(rate, 1, 1)
        
        grid_layout.addWidget(QLabel("Discount: "), 2, 0)
        grid_layout.addWidget(discount1, 2, 1)

        button_layout = QHBoxLayout()
        remove_item_from_cart = QPushButton(text = "Remove from cart")
        remove_item_from_cart.clicked.connect(lambda: self.remove_item_from_cart(row))

        discard_changes = QPushButton(text = "Discard")
        discard_changes.clicked.connect(self.close_item_manipulation_popup)

        apply_changes = QPushButton(text = "Apply")
        apply_changes.clicked.connect(lambda: self.update_cart_item(row, quantity_input.text(), rate.text(), discount1.text()))
        button_layout.addWidget(remove_item_from_cart)
        button_layout.addWidget(discard_changes)
        button_layout.addWidget(apply_changes)
    
            
        popup_layout = QVBoxLayout()
        popup_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        popup_layout.setSpacing(0)
        popup_layout.setContentsMargins(0,0,0,0)
        popup_layout.addWidget(self.title_bar)
        popup_layout.addWidget(name_label)
        popup_layout.addLayout(grid_layout)
        popup_layout.addStretch()
        popup_layout.addLayout(button_layout)

        screen_height = self.store_ui.height()
        screen_width = self.store_ui.width()

        popup_width = 375
        popup_height = 350
        popup_x = (screen_width - popup_width) // 2  # Center horizontally
        popup_y = (screen_height - popup_height) // 2  # Position below the top bar
        self.item_manipulation_popup.setGeometry(popup_x, popup_y, popup_width, popup_height)
        self.item_manipulation_popup.setLayout(popup_layout)
        self.item_manipulation_popup.setParent(self.store_ui)
        self.item_manipulation_popup.show()
        self.item_manipulation_popup.raise_()        
       
    def update_cart_item(self, row, quantity, price, discount):
        print(f"Discount: {discount}")

        if float(discount) > float(price):
            QMessageBox.warning(self, "Invalid Discount", "Discount cannot exceed the price!")
            return

        item_cell = self.table.item(row, 1)
        if item_cell is None:
            QMessageBox.warning(self, "Error", "Invalid item selection!")
            return

        item_name = item_cell.text().strip()
        
        if item_name not in self.cart_items:
            print(f"Item '{item_name}' not found in cart_items!")
            print("Current cart_items:", self.cart_items)
            return

        # Update cart dictionary
        self.cart_items[item_name]["quantity"] = float(quantity)
        self.cart_items[item_name]["price"] = float(price)
        self.cart_items[item_name]["discount"] = float(discount)
        self.cart_items[item_name]["total"] = float(quantity) * (float(price) - float(discount))

        # Update UI
        self.table.item(row, 2).setText(str(quantity))
        self.table.item(row, 3).setText(str(price))
        self.table.item(row, 4).setText(str(discount))
        self.table.item(row, 5).setText(str(float(quantity) * (float(price) - float(discount))))

        # Debugging
        print("Updated cart_items:", self.cart_items)

        self.parent.update_summary()
        self.close_item_manipulation_popup()


                                                                  
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

        # Connect signal to show add_item_popup
        name_edit.textEdited.connect(lambda: self.show_add_item_popup(name_edit))

    def show_add_item_popup(self, name_edit):
        """Shows the Add Item add_item_popup when typing in the name field."""
        self.store_ui.toggle_overlay(True)  # Show overlay
        self.store_ui.overlayClicked.connect(self.close_add_item_popup)

        # Set add_item_popup position just below the top bar
        margin_top = 60  # Adjust based on top bar height
        screen_width = self.store_ui.width()
        
        self.add_item_popup = QWidget(self)

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

        self.popupLayout = QVBoxLayout(self.add_item_popup)
        self.popupLayout.addWidget(self.popupSearchBar)
        self.popupLayout.addWidget(self.scroll_area)

        self.add_item_popup.setGeometry(popup_x, popup_y, popup_width, popup_height)
        self.add_item_popup.setStyleSheet("background-color: white; border-radius: 10px; color:  black;")
        
        self.add_item_popup.setParent(self.store_ui)  # Ensure it belongs to main window
        self.add_item_popup.show()
        self.popupSearchBar.setFocus()
        self.add_item_popup.raise_()  # 🔥 Ensure it's above the overlay

        self.load_popup_items(self.popupSearchBar.text().strip())

    def close_add_item_popup(self):
        """Closes the add_item_popup and hides the overlay."""
        if hasattr(self, "add_item_popup"):
            self.add_item_popup.close()
            del self.add_item_popup
            self.store_ui.toggle_overlay(False)  # Hide overlay

    def close_item_manipulation_popup(self):
        """Closes the item_manipulation_popup and hides the overlay."""
        if hasattr(self, "item_manipulation_popup"):
            self.item_manipulation_popup.close()
            self.item_manipulation_popup.lower()
            del self.item_manipulation_popup
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
        """Loads add_item_popup items into the UI with search filtering."""
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
        self.close_add_item_popup()

    def clear_cart(self, force=False):
        """Clears all items from the cart after user confirmation."""
        if force is True and self.table.rowCount() !=0:
            self.table.setRowCount(0)
            self.cart_items.clear()
            self.parent.update_summary()
            # Re-add an empty row for a new entry
            self.add_empty_row()
            return

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
            self.parent.update_summary()
            # Re-add an empty row for a new entry
            self.add_empty_row()


class popupItemWidget(QFrame):
    double_clicked = pyqtSignal(object) 
    def __init__(self, item_data, parent=None):
        super().__init__(parent)

        self.setObjectName("popupItemWidget")

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
        



