from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QCompleter, QHeaderView, QApplication
)
from PySide6.QtCore import Qt

class CartTable(QWidget):
    def __init__(self):
        super().__init__()

        # Sample product list for search
        self.products = {
            "Chips": 20, "Cookies": 30, "Soda": 50, "Juice": 40, "Candy": 10
        }

        # Main Layout
        self.layout = QVBoxLayout(self)

        # Search Bar with Auto-Suggestions
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Type here to add an item ")
        self.search_completer = QCompleter(list(self.products.keys()), self)
        self.search_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_bar.setCompleter(self.search_completer)
        self.search_bar.returnPressed.connect(self.add_item_to_cart)

        # Cart Table (6 Columns: No, Name, MRP, Quantity, Discount, Amount)
        self.cart_table = QTableWidget(0, 6, self)
        self.cart_table.setHorizontalHeaderLabels(["NO", "Name", "MRP", "Quantity", "Discount", "Amount"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Add widgets to layout
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.cart_table)

    def add_item_to_cart(self):
        """Add selected product to the cart table."""
        item_name = self.search_bar.text().strip()
        if item_name and item_name in self.products:
            row = self.cart_table.rowCount()
            self.cart_table.insertRow(row)

            # Auto-fill table columns
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))  # NO
            self.cart_table.setItem(row, 1, QTableWidgetItem(item_name))     # Name
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(self.products[item_name])))  # MRP
            self.cart_table.setItem(row, 3, QTableWidgetItem("1"))           # Quantity (default 1)
            self.cart_table.setItem(row, 4, QTableWidgetItem("0"))           # Discount (default 0)
            self.cart_table.setItem(row, 5, QTableWidgetItem(str(self.products[item_name])))  # Amount
            
            self.cart_table.itemChanged.connect(self.update_amount)  # Auto-update amount
            self.search_bar.clear()  # Clear search bar for next entry

    def update_amount(self):
        """Recalculate amount when Quantity or Discount changes."""
        for row in range(self.cart_table.rowCount()):
            try:
                mrp = float(self.cart_table.item(row, 2).text())
                quantity = int(self.cart_table.item(row, 3).text())
                discount = float(self.cart_table.item(row, 4).text())
                amount = (mrp - discount) * quantity
                self.cart_table.setItem(row, 5, QTableWidgetItem(str(amount)))
            except ValueError:
                pass  # Ignore invalid input

if __name__ == "__main__":
    app = QApplication([])
    window = CartTable()
    window.show()
    app.exec()
