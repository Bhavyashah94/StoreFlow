from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt

class TransactionsPanel(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db  

        self.setObjectName("transactions_panel")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # Defining columns
        self.table = QTableWidget(0, 9)  
        self.table.setHorizontalHeaderLabels(["Item Name", "Transaction Type", "Time Stamp", "Payment Mode", "Reference No.", "Quantity",
                                               "Price", "Discount", "Total"])

        # Resizing Columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.table)

        self.load_transactions()

    # To load existing transactions from db
    def load_transactions(self):
        transactions = self.db.get_transactions()

        self.table.setRowCount(0)

        for trans in transactions:  # Trans people 🤭
            self.add_transaction(trans) 

    def add_transaction(self, transaction):
        row = self.table.rowCount()
        self.table.insertRow(row)  # New row dynamically
        
        if transaction["transaction_type"] == 'adjustment':
            self.table.setItem(row, 0, QTableWidgetItem(transaction["inventory_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(transaction["transaction_type"]))
            timestamp_str = transaction["timestamp"].toString("yyyy-MM-dd hh:mm:ss") if hasattr(transaction["timestamp"], "toString") else str(transaction["timestamp"])
            self.table.setItem(row, 2, QTableWidgetItem(timestamp_str))
            self.table.setItem(row, 3, QTableWidgetItem(transaction["reference_no"]))
            self.table.setSpan(row, 3, 1, 6)
        
        else:
            self.table.setItem(row, 0, QTableWidgetItem(transaction["inventory_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(transaction["transaction_type"]))
            self.table.setItem(row, 3, QTableWidgetItem(transaction["payment_mode"]))
            timestamp_str = transaction["timestamp"].toString("yyyy-MM-dd hh:mm:ss") if hasattr(transaction["timestamp"], "toString") else str(transaction["timestamp"])
            self.table.setItem(row, 2, QTableWidgetItem(timestamp_str))
            self.table.setItem(row, 4, QTableWidgetItem(transaction["reference_no"]))
            self.table.setItem(row, 5, QTableWidgetItem(str(transaction["quantity"])))
            self.table.setItem(row, 6, QTableWidgetItem(str(transaction["price"])))
            self.table.setItem(row, 7, QTableWidgetItem(str(transaction["discount"])))
            self.table.setItem(row, 8, QTableWidgetItem(str(int(transaction["quantity"]) * (transaction["price"] - transaction["discount"]))))