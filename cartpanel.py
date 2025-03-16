from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QWidget
)
from PyQt6.QtCore import Qt

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
        self.cart_table = CartTable(store_ui)
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

        # 🔹 **Sales Summary Title**
        self.sales_summary_label = QLabel("<b>Sales Summary</b>")
        self.sales_summary_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.summary_layout.addWidget(self.sales_summary_label)

        # 🔹 **Sales Summary Labels**
        self.sub_total_label = QLabel("Subtotal: ₹0.00")
        self.discount_info_label = QLabel("<i>(Item discount included: ₹0.00)</i>")
        self.discount_info_label.setStyleSheet("color: gray; font-size: 12px;")  # Light gray text
        self.round_off_label = QLabel("Round Off: ₹0.00")
        self.total_label = QLabel("<b>Total: ₹0.00</b>")  # Bold total

        # 🔹 **Adding Labels to Layout**
        self.summary_layout.addWidget(self.sub_total_label)
        self.summary_layout.addWidget(self.discount_info_label)
        self.summary_layout.addWidget(self.round_off_label)
        self.summary_layout.addWidget(self.total_label)

        # 📌 **Payment Options (Like Zakya)**
        self.payment_button_layout = QVBoxLayout()
        self.payment_button_layout.setSpacing(5)

        self.cash_btn = QPushButton("Cash ")
        self.card_btn = QPushButton("Card ")
        self.upi_btn = QPushButton("UPI ")
        self.credit_sale_btn = QPushButton("Credit Sale ")
        self.split_payment_btn = QPushButton("Split Payment ")

        for btn in [self.cash_btn, self.card_btn, self.upi_btn, self.credit_sale_btn, self.split_payment_btn]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.payment_button_layout.addWidget(btn)

        # 🔹 **Add Payment Buttons to Summary Layout**
        self.summary_layout.addLayout(self.payment_button_layout)

        # 📌 **Add Sections to Main Layout**
        self.layout.addWidget(self.cart_list, stretch=7)
        self.layout.addWidget(self.cart_summary, stretch=3)
        self.setLayout(self.layout)

    def fetch_sales_summary(self):
        """Fetch latest sales summary from the database"""
        from database import Database  # Import Database class
        db = Database()  # Create an instance of Database    

        summary_data = db.get_sales_summary()  # Fetch sales summary
        return summary_data if summary_data else {"sub_total": 0, "discount": 0, "round_off": 0, "total": 0}

    def update_sales_summary(self):
        """Update the sales summary panel with data from the database"""
        summary_data = self.fetch_sales_summary()

        self.sub_total_label.setText(f"Subtotal: ₹{summary_data['sub_total']:.2f}")
        self.discount_info_label.setText(f"<i>(Item discount included: ₹{summary_data['discount']:.2f})</i>")
        self.round_off_label.setText(f"Round Off: ₹{summary_data['round_off']:.2f}")
        self.total_label.setText(f"<b>Total: ₹{summary_data['total']:.2f}</b>")

    def clearCart(self):
        self.cart_table.clear_cart()
        self.update_sales_summary()
