from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QWidget, QGridLayout, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from CartTable import CartTable
from database import Database
from datetime import datetime
from receiptpopup import ReceiptPopup

class CartPanel(QFrame):
    def __init__(self, store_ui):
        super().__init__()
        self.setObjectName("cart_panel")

        self.store_ui = store_ui
        self.database = Database()

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
        
        self.cash_btn.clicked.connect(lambda: self.show_payment_popup("Cash"))
        self.card_btn.clicked.connect(lambda: self.show_payment_popup("Credit"))
        self.upi_btn.clicked.connect(lambda: self.show_payment_popup("UPI"))

        for btn in [self.cash_btn, self.card_btn, self.upi_btn]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.payment_button_layout.addWidget(btn)

        self.summary_layout.addLayout(self.payment_button_layout)

        self.layout.addWidget(self.cart_list, stretch=7)
        self.layout.addWidget(self.cart_summary, stretch=3)
        self.setLayout(self.layout)

        # Setup Payment Popup
        self.setup_payment_popup()

        self.store_ui.overlayClicked.connect(self.close_payment_popup)

    def clearCart(self):
        self.cart_table.clear_cart()

    def update_summary(self):
        total_sub_price = 0
        total_price = 0.0
        total_discount = 0.00

        for row in range(self.cart_table.table.rowCount()):
            qty_item = self.cart_table.table.item(row, 2)
            price_item = self.cart_table.table.item(row, 3)
            discount_item = self.cart_table.table.item(row, 4)
            
            if qty_item and price_item:
                try:
                    qty = int(qty_item.text())
                    price = float(price_item.text())
                    discount = float(discount_item.text())
                    total_sub_price += price
                    total_discount += discount
                    total_price += qty * price - discount
                except ValueError:
                    continue

        self.sub_total.setText(str(total_sub_price))
        self.total_discount.setText(str(total_discount))
        self.total.setText(str(total_price))

    def setup_payment_popup(self):
        """Creates the payment popup UI."""
        self.payment_popup = QFrame(self)
        self.payment_popup.setObjectName("payment_popup")
        self.payment_popup.setStyleSheet("""
            #payment_popup {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
        """)
        self.payment_popup.setFixedSize(300, 200)
        self.payment_popup.setVisible(False)

        layout = QVBoxLayout(self.payment_popup)

        self.payment_title = QLabel("Payment")
        self.payment_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.payment_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        self.payment_details = QLabel("Total: ₹0.00")
        self.payment_details.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.payment_input = QLineEdit()
        self.payment_input.setPlaceholderText("Enter amount/reference")
        self.payment_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tender_button = QPushButton("Tender")
        self.tender_button.clicked.connect(self.process_payment)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_payment_popup)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.tender_button)

        layout.addWidget(self.payment_title)
        layout.addWidget(self.payment_details)
        layout.addWidget(self.payment_input)
        layout.addLayout(button_layout)

        self.payment_popup.setLayout(layout)

    def show_payment_popup(self, method):
        """Displays the payment popup with overlay."""

        self.selected_payment_mode = method

        self.store_ui.toggle_overlay(True)
        self.payment_title.setText(f"{method} Payment")
        self.payment_details.setText(f"Total: ₹{self.total.text()}")

        self.payment_input.setPlaceholderText(
            "Enter amount given" if method == "Cash" else "Enter reference number"
        )

        self.payment_popup.move(
            (self.width() - self.payment_popup.width()) // 2,
            (self.height() - self.payment_popup.height()) // 2
        )
        self.payment_popup.setParent(self.store_ui)
        
        self.payment_popup.show()
        self.payment_popup.raise_()

    def close_payment_popup(self):
        """Hides the payment popup and overlay."""
        self.payment_popup.hide()
        self.payment_popup.lower()

        self.store_ui.toggle_overlay(False)

    def process_payment(self):
        """Handles payment processing when the tender button is clicked."""
        if not hasattr(self, "payment_input") or not self.payment_input:
            print("❌ Payment input field is missing!")
            return

        amount = self.payment_input.text().strip()
        if not amount:
            print("⚠️ Please enter an amount or reference number.")
            return

        try:
            amount_value = float(amount)
            if amount_value <= 0:
                print("⚠️ Invalid payment amount.")
                return
        except ValueError:
            print("⚠️ Invalid input. Please enter a valid number.")
            return

        print(f"✅ Processing payment of ₹{amount_value}")

        if not self.cart_table.cart_items:
            print("❌ Cart is empty!")
            return

        transaction_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction_id = f"TXN{int(datetime.now().timestamp())}"  # Unique transaction ID

        subtotal = sum(item["quantity"] * item["price"] - item["discount"] for item in self.cart_table.cart_items.values())
        total_discount = sum(item["discount"] for item in self.cart_table.cart_items.values())
        final_total = subtotal - total_discount

        success = True
        purchased_items = []

        for inventory_name, item in self.cart_table.cart_items.items():
            quantity = item.get("quantity")
            price = item.get("price")
            discount = item.get("discount")
            total_price = (price - discount) * quantity

            if not self.database.record_transaction(
                inventory_name=inventory_name,
                transaction_type="sale",
                quantity=quantity,
                price=price,
                discount=discount,
                payment_mode=self.selected_payment_mode,
                cash_received=amount_value if self.selected_payment_mode == "cash" else None,
                return_amount=amount_value - final_total if self.selected_payment_mode == "cash" else None,
                reference_no=amount if self.selected_payment_mode in ["credit", "UPI"] else None,
                timestamp = transaction_timestamp
            ):
                success = False
                print(f"❌ Failed to save transaction for {inventory_name}.")
                continue

            purchased_items.append({
                "name": inventory_name,
                "quantity": quantity,
                "price": price,
                "discount": discount,
                "total": total_price
            })

        if success:
            print("✅ All transactions saved successfully.")
            
            # Generate transaction details for receipt
            transaction_details = {
                "store_name": "ABC Supermarket",
                "store_address": "123 Market Road, City",
                "store_contact": "9876543210",
                "transaction_id": transaction_id,
                "date_time": transaction_timestamp,
                "payment_mode": self.selected_payment_mode,
                "reference_no": amount if self.selected_payment_mode in ["credit", "UPI"] else None,
                "items": purchased_items,
                "subtotal": subtotal,
                "total_discount": total_discount,
                "final_total": final_total,
                "cash_received": amount_value if self.selected_payment_mode == "cash" else None,
                "return_amount": amount_value - final_total if self.selected_payment_mode == "cash" else None
            }

            self.close_payment_popup()  # Close payment UI
            self.cart_table.clear_cart(True)
            # Show receipt popup
            self.receipt_popup = ReceiptPopup(self, transaction_details)
            self.receipt_popup.exec()

        else:
            print("⚠️ Some transactions failed. Please check logs.")



