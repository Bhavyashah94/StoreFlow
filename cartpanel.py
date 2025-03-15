from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt

from CartTable import CartTable

class CartPanel(QFrame):
    def __init__(self, store_ui):
        super().__init__()
        self.setObjectName("cart_panel")

        # Layout for Cart Panel
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 🛒 **Cart List (70%)**
        self.cart_list = QFrame(self)
        self.cart_list.setObjectName("cart_list")
        self.cart_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Vertical Layout for Cart List
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
        self.cart_summary.setFixedWidth(500)

        # Layout for Cart Summary
        self.summary_layout = QVBoxLayout(self.cart_summary)
        self.summary_layout.setContentsMargins(10, 10, 10, 10)
        self.summary_layout.setSpacing(10)

        self.total_label = QLabel("Total: ₹0.00")
        self.total_label.setObjectName("cart_total_label")
        self.summary_layout.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Add both panels to the main layout
        self.layout.addWidget(self.cart_list, stretch=7)
        self.layout.addWidget(self.cart_summary, stretch=3)

        self.setLayout(self.layout)

    def clearCart(self):
        self.cart_table.clear_cart()

