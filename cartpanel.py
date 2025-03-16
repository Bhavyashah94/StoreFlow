from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QWidget, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from CartTable import CartTable

class CartPanel(QFrame):
    def __init__(self, store_ui):
        super().__init__()
        self.setObjectName("cart_panel")

        # 🛒 **Main Layout**
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 📌 **Cart List Section (70%)**
        self.cart_list = QFrame(self)
        self.cart_list.setObjectName("cart_list")
        self.cart_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.cart_layout = QVBoxLayout(self.cart_list)
        self.cart_layout.setContentsMargins(0, 0, 0, 0)
        self.cart_layout.setSpacing(0)

        # ✅ **Cart Table**
        self.cart_table = CartTable(store_ui, self)
        self.cart_layout.addWidget(self.cart_table)

        # Buttons (Clear Cart & Hold Cart)
        self.button_frame = QFrame(self.cart_list)
        self.button_frame.setObjectName("cart_buttons")
        self.button_layout = QHBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.button_layout.setSpacing(10)

        self.clear_cart_btn = QPushButton("Clear Cart")
        self.clear_cart_btn.setObjectName("clear_cart_btn")
        self.clear_cart_btn.clicked.connect(self.clearCart)

        self.hold_cart_btn = QPushButton("Hold Cart")
        self.hold_cart_btn.setObjectName("hold_cart_btn")

        self.button_layout.addWidget(self.clear_cart_btn)
        self.button_layout.addWidget(self.hold_cart_btn)
        self.button_layout.addStretch()

        self.cart_layout.addWidget(self.button_frame)

        # 📊 **Cart Summary (30%)**
        self.cart_summary = QFrame(self)
        self.cart_summary.setObjectName("cart_summary")
        self.cart_summary.setFixedWidth(450)  # Adjust width

        # ✅ **Sales Summary Container**
        self.summary_layout = QVBoxLayout(self.cart_summary)
        self.summary_layout.setContentsMargins(10, 10, 10, 10)
        self.summary_layout.setSpacing(10)

        self.summary_layout.addStretch()

        self.sub_total = QLabel()
        self.total_discount = QLabel()
        self.round_off = QLabel()
        self.total = QLabel()

        self.sub_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.total_discount.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.round_off.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.total.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.grid_layout = QGridLayout()

        self.grid_layout.addWidget(QLabel("Sub-Total: "), 0, 0)
        self.grid_layout.addWidget(self.sub_total, 0, 1)
        
        self.grid_layout.addWidget(QLabel("Discount: "), 1, 0)
        self.grid_layout.addWidget(self.total_discount, 1, 1)
        
        self.grid_layout.addWidget(QLabel("Round Off: "), 2, 0)
        self.grid_layout.addWidget(self.round_off, 2, 1)
        
        self.grid_layout.addWidget(QLabel("Total: "), 3, 0)
        self.grid_layout.addWidget(self.total, 3, 1)

        self.sales_summary_label = QLabel("<b>Sales Summary</b>")
        self.sales_summary_label.setStyleSheet("font-size: 20px")
        self.summary_layout.addWidget(self.sales_summary_label)

        self.summary_layout.addLayout(self.grid_layout)

        self.payment_button_layout = QHBoxLayout()
        self.payment_button_layout.setSpacing(5)

        self.cash_btn = QPushButton("Cash ")
        self.card_btn = QPushButton("Card ")
        self.upi_btn = QPushButton("UPI ")

        for btn in [self.cash_btn, self.card_btn, self.upi_btn]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.payment_button_layout.addWidget(btn)

        # 🔹 **Add Payment Buttons to Summary Layout**
        self.summary_layout.addLayout(self.payment_button_layout)

        # 📌 **Add Sections to Main Layout**
        self.layout.addWidget(self.cart_list, stretch=7)
        self.layout.addWidget(self.cart_summary, stretch=3)
        self.setLayout(self.layout)

    def clearCart(self):
        self.cart_table.clear_cart()

    def update_summary(self):
        total_sub_price = 0
        total_price = 0.0
        total_discount = 0.00

        for row in range(self.cart_table.table.rowCount()):
            qty_item = self.cart_table.table.item(row, 2)  # Adjust column index
            price_item = self.cart_table.table.item(row, 3)  # Adjust column index
            discount_item = self.cart_table.table.item(row, 4)  # Adjust column index
            
            if qty_item and price_item:
                try:
                    qty = int(qty_item.text())
                    price = float(price_item.text())
                    discount = float(discount_item.text())
                    total_sub_price += price
                    total_discount += discount
                    total_price += qty * price - discount
                except ValueError:
                    continue  # Ignore invalid entries

        # Update the summary labels
        self.sub_total.setText(str(total_sub_price))
        self.total_discount.setText(str(total_discount))
        self.total.setText(str(total_price))


