from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QApplication
)
from PyQt6.QtCore import Qt


class CartTable(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout(self)

        # Cart Table (6 columns: 1 for fake vertical header, 5 for actual data)
        self.table = QTableWidget(0, 6)  # Extra column for row numbering
        self.table.setHorizontalHeaderLabels(["NO", "Item Name", "Quantity", "Price", "Discount", "Total"])

        # Hide the actual vertical header
        self.table.verticalHeader().setVisible(False)

        # Style the first column (Fake vertical header)
        self.table.setColumnWidth(0, 50)  # Adjust width as needed
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)

        # Set other column sizes
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # "Item Name"
        for i in range(2, 6):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(i, 100)

        # Disable editing
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Add table to layout
        self.layout.addWidget(self.table)

        # Add test items
        self.add_cart_item("Apple", 2, "$3.00", "$0.50", "$5.50")
        self.add_cart_item("Apple", 2, "$3.00", "$0.50", "$5.50")
        self.add_cart_item("Banana", 5, "$1.50", "$0.00", "$7.50")


    def update_row_numbers(self):
        """Updates the numbering in the first column after adding/removing rows."""
        for row in range(self.table.rowCount()):
            item = QTableWidgetItem(str(row + 1))  # Numbering starts from 1
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item)

    def add_cart_item(self, item_name, quantity, price, discount, total):
        """Adds an item to the cart table."""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # Add fake vertical header number
        self.update_row_numbers()

        # Add actual data
        self.table.setItem(row_count, 1, QTableWidgetItem(item_name))
        self.table.setItem(row_count, 2, QTableWidgetItem(str(quantity)))
        self.table.setItem(row_count, 3, QTableWidgetItem(price))
        self.table.setItem(row_count, 4, QTableWidgetItem(discount))
        self.table.setItem(row_count, 5, QTableWidgetItem(total))

    def remove_selected_item(self):
        """Removes the selected row and updates numbering."""
        selected_rows = set(index.row() for index in self.table.selectedIndexes())  # Get selected row numbers
        for row in sorted(selected_rows, reverse=True):  # Remove from bottom to top
            self.table.removeRow(row)

        self.update_row_numbers()  # Refresh numbering


# Testing the Cart Table
if __name__ == "__main__":
    app = QApplication([])
    window = CartTable()
    window.show()
    app.exec()
