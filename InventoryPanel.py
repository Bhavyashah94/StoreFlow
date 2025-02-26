from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt, QEvent

class InventoryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("inventory_panel")

        # Main layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  
        self.layout.setSpacing(0)

        # Inventory List
        self.inventory_list = QFrame(self)
        self.inventory_list.setObjectName("inventory_list")
        self.inventory_list.setFixedWidth(500)
        
        #Inventory Info/Details/Addnew/Edit
        self.inventory_info = QStackedWidget(self)
        self.inventory_info.setObjectName("inventory_info")

        self.layout.addWidget(self.inventory_list)
        self.layout.addWidget(self.inventory_info)

        
        
