from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QGuiApplication
import sys

from cartpanel import CartPanel
from InventoryPanel import InventoryPanel
from TransactionsPanel import TransactionsPanel
from database import Database

class StoreFlowUI(QWidget):
    overlayClicked = pyqtSignal()  # Signal emitted when overlay is clicked

    def __init__(self):
        super().__init__()

        self.setWindowTitle("StoreFlow")
        self.showFullScreen()
        self.load_stylesheet("theme.qss")

        # Top Bar
        self.top_bar = QFrame(self)
        self.top_bar.setObjectName("top_bar")
        self.top_bar.setFixedHeight(50)

        self.toggle_button = QPushButton("☰")
        self.toggle_button.setObjectName("toggle_button")
        self.toggle_button.setFixedSize(50, 50)
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        self.top_bar_title = QLabel("StoreFlow: Cart")
        self.top_bar_title.setObjectName("top_bar_label")
        self.top_bar_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Overlay (Dark Background)
        self.overlay = QWidget(self)
        self.overlay.setObjectName("overlay")
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 100);")  # Semi-transparent
        self.overlay.hide()

        # Capture clicks on overlay
        self.overlay.mousePressEvent = self.on_overlay_clicked

        # Sidebar (Floating)
        self.sidebar = QFrame(self)
        self.sidebar.setObjectName("side_bar")
        self.sidebar.setFixedWidth(200)
        self.sidebar.setFixedHeight(self.height())  # Full height
        self.sidebar.move(-200, 0)  # Initially hidden (off-screen)

        # Sidebar Layout
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        # Panel Switcher (QStackedWidget)
        self.panel_manager = QStackedWidget(self)
        self.panel_manager.setObjectName("panel_manager")

        # Create Panels
        self.cart_panel = CartPanel(self)
        self.inventory_panel = InventoryPanel(self)
        self.db = Database()
        self.transactions_panel = TransactionsPanel(self.db)
        self.settings_panel = QLabel("Settings Panel", self)

        # Add panels to QStackedWidget
        self.panel_manager.addWidget(self.cart_panel)
        self.panel_manager.addWidget(self.inventory_panel)
        self.panel_manager.addWidget(self.transactions_panel)
        self.panel_manager.addWidget(self.settings_panel)

        # Sidebar Buttons
        button_names = [("Cart", 0), ("Inventory", 1), ("Transactions", 2)]
        for name, index in button_names:
            btn = QPushButton(name)
            btn.setObjectName("sidebar_button")

            # Use lambda for dynamic binding
            btn.clicked.connect(lambda _, i=index, n=name: self.switch_panel(i, n))

            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()

        # Top Bar Layout
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.addWidget(self.toggle_button)
        self.top_bar_layout.addWidget(self.top_bar_title)
        self.top_bar_layout.addStretch()

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addWidget(self.panel_manager)

        self.setLayout(self.main_layout)

        # connecting Overlay to sidebar
        self.overlayClicked.connect(lambda: self.toggle_sidebar(True))

        # Install event filter to detect Esc key
        app.installEventFilter(self)

        # Sidebar State
        self.sidebar_visible = False

    def toggle_sidebar(self, force_close=False):
        """Toggles the sidebar and overlay"""
        if self.sidebar_visible or force_close:
            self.sidebar.hide()
            self.toggle_overlay(False)  # Hide overlay
            self.sidebar_visible = False
        else:
            self.sidebar.setGeometry(0, 50, 200, self.height())  # Ensure correct position
            self.sidebar.show()
            self.toggle_overlay(True)  # Show overlay
            self.sidebar.raise_()
            self.sidebar_visible = True

    def on_overlay_clicked(self, event):
        """Emits a signal when the overlay is clicked."""
        self.overlayClicked.emit()
        self.toggle_overlay(False)  # Hide overlay on click

    def toggle_overlay(self, show=True):
        """Shows or hides the overlay."""
        if show:
            self.overlay.setGeometry(0, 0, self.width(), self.height())
            self.overlay.show()
            self.overlay.raise_()
        else:
            self.overlay.lower()
            self.overlay.hide()

    def load_stylesheet(self, filename):
        """Loads QSS stylesheet."""
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())

    def eventFilter(self, obj, event):
        """Detect Esc key press to close the sidebar."""
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            if self.sidebar_visible:
                self.toggle_sidebar(force_close=True)  # Close sidebar if open
            else:
                self.close()  # Close the app
            return True
        return super().eventFilter(obj, event)

    def switch_panel(self, index, name):
        """Handles panel switching with cart clearance confirmation."""
        if self.panel_manager.currentIndex() == 0:  # If switching from Cart
            if self.cart_panel.cart_table.table.rowCount() > 1:  # Check if cart has items
                confirm = QMessageBox(self)
                confirm.setWindowTitle("Confirm Clear")
                confirm.setText("You have items in your cart. Clear the cart before switching?")
                confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if confirm.exec() == QMessageBox.StandardButton.Yes:
                    self.cart_panel.cart_table.table.setRowCount(0)  # Clear cart
                    self.cart_panel.cart_table.update_row_numbers()
                    self.cart_panel.cart_table.add_empty_row()
                else:
                    return  # Cancel switch if user selects No

        # Proceed with panel switch
        self.inventory_panel.load_inventory_items("")  # Refresh inventory panel
        self.transactions_panel.load_transactions()
        self.panel_manager.setCurrentIndex(index)
        self.toggle_sidebar(force_close=True)
        self.top_bar_title.setText(f"StoreFlow: {name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StoreFlowUI()
    window.show()
    sys.exit(app.exec())
