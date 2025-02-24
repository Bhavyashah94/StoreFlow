from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QEvent
import sys

class StoreFlowUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StoreFlow")
        self.showFullScreen()

        # Load QSS theme
        self.load_stylesheet("theme.qss")

        # Top Bar
        self.top_bar = QFrame(self)
        self.top_bar.setObjectName("top_bar")
        self.top_bar.setFixedHeight(50)

        # Toggle Sidebar Button
        self.toggle_button = QPushButton("☰")
        self.toggle_button.setObjectName("toggle_button")
        self.toggle_button.setFixedSize(50, 50)
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # Sidebar
        self.sidebar = QFrame(self)
        self.sidebar.setObjectName("side_bar")
        self.sidebar.setFixedWidth(200)

        # Sidebar Buttons
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        button_names = ["Cart", "Inventory", "Sales", "Settings"]
        for name in button_names:
            btn = QPushButton(name)
            btn.setObjectName("sidebar_button")
            self.sidebar_layout.addWidget(btn)
        self.sidebar_layout.addStretch()

        # Main Content
        self.main_content = QFrame(self)
        self.main_content.setObjectName("main_content")
        self.main_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Layouts
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.addWidget(self.toggle_button)
        self.top_bar_layout.addStretch()

        # Content Layout (Holds Sidebar + Main Content)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.addWidget(self.sidebar)
        self.content_layout.addWidget(self.main_content)

        # Main Layout (Holds Top Bar + Content Layout)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addLayout(self.content_layout)

        self.setLayout(self.main_layout)

        # Install event filter to detect Esc key
        app.installEventFilter(self)

    def toggle_sidebar(self):
        """Toggles the visibility of the sidebar."""
        if self.sidebar.isVisible():
            self.sidebar.hide()
            self.toggle_button.setText("☰")
        else:
            self.sidebar.show()
            self.toggle_button.setText("✖")

    def load_stylesheet(self, filename):
        """Loads QSS stylesheet."""
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())

    def eventFilter(self, obj, event):
        """Detect Esc key press to close the app."""
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.close()  # Close the window when Esc is pressed
            return True
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StoreFlowUI()
    window.show()
    sys.exit(app.exec())
