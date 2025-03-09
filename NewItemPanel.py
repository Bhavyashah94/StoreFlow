from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database import Database  # Import database connection

class NewItemPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()  # Initialize the database connection

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.gtin_input = QLineEdit(self)
        self.unit_input = QLineEdit(self)
        self.selling_price_input = QLineEdit(self)
        self.mrp_input = QLineEdit(self)
        self.cost_price_input = QLineEdit(self)
        self.stock_input = QLineEdit(self)
        self.reorder_input = QLineEdit(self)

        self.add_button = QPushButton("Add Item", self)
        self.add_button.clicked.connect(self.add_item_to_db)

        for label, input_field in [
            ("Name:", self.name_input),
            ("GTIN:", self.gtin_input),
            ("Unit:", self.unit_input),
            ("Selling Price:", self.selling_price_input),
            ("MRP:", self.mrp_input),
            ("Cost Price:", self.cost_price_input),
            ("Stock:", self.stock_input),
            ("Reorder Point:", self.reorder_input)
        ]:
            self.layout.addWidget(QLabel(label))
            self.layout.addWidget(input_field)

        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)

    def add_item_to_db(self):
        """Fetch user input and call add_item"""
        name = self.name_input.text()
        gtin = self.gtin_input.text()
        unit = self.unit_input.text()

        try:
            selling_price = float(self.selling_price_input.text())
            mrp = float(self.mrp_input.text())
            cost_price = float(self.cost_price_input.text())
            stock = float(self.stock_input.text())
            reorder_point = float(self.reorder_input.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numeric values.")
            return

        success = self.db.add_item(name, gtin, unit, selling_price, mrp, cost_price, stock, reorder_point)
        
        if success:
            QMessageBox.information(self, "Success", "Item added successfully!")
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add item. Duplicate GTIN or Name?")

    def clear_inputs(self):
        """Clear input fields after successful entry"""
        self.name_input.clear()
        self.gtin_input.clear()
        self.unit_input.clear()
        self.selling_price_input.clear()
        self.mrp_input.clear()
        self.cost_price_input.clear()
        self.stock_input.clear()
        self.reorder_input.clear()
