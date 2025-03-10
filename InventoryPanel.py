from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                            QLabel, QLineEdit, QFormLayout, QStackedWidget, QGridLayout, QComboBox, QProgressDialog)
from PyQt6.QtCore import Qt, QRegularExpression, QThread, pyqtSlot

from PyQt6.QtGui import QRegularExpressionValidator
from database import Database




class AddNewInventoryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setObjectName("add_new_inventory_panel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 400, 10)
        layout.setSpacing(10)
        
        self.new_item_label = QLabel("New Item")
        self.new_item_label.setObjectName("new_item_label")
        self.new_item_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        # Basic Information Section
        self.basic_info_frame = QFrame(self)
        self.basic_info_frame.setStyleSheet("background-color: #d0e8ff; border-radius: 8px; padding: 10px;")
        self.basic_info_vlayout = QVBoxLayout(self.basic_info_frame)

        self.basic_info_label = QLabel("Basic Information")
        self.basic_info_label.setStyleSheet("font-weight: bold; color: #0056b3;")

        self.basic_info_fields = QGridLayout()
        label_width = 180  

        self.name_label = QLabel("Name:")
        self.name_label.setFixedWidth(label_width)
        self.name_input = QLineEdit()
        self.name_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"^[^\s].*")))

        self.gstn_label = QLabel("gtin Number:")
        self.gstn_label.setFixedWidth(label_width)
        self.gstn_input = QLineEdit()
        self.gstn_input.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]{13}$")))

        self.unit_label = QLabel("Unit of Measurement:")
        self.unit_label.setFixedWidth(label_width)
        self.unit_input = QComboBox()
        self.unit_input.setEditable(False)
        self.unit_input.setPlaceholderText("Select a Unit")  
        self.unit_input.addItem("Kg")
        self.unit_input.addItem("gms")
        self.unit_input.addItem("Pcs")

        self.basic_info_fields.addWidget(self.name_label, 0, 0)
        self.basic_info_fields.addWidget(self.name_input, 0, 1)
        self.basic_info_fields.addWidget(self.gstn_label, 1, 0)
        self.basic_info_fields.addWidget(self.gstn_input, 1, 1)
        self.basic_info_fields.addWidget(self.unit_label, 2, 0)
        self.basic_info_fields.addWidget(self.unit_input, 2, 1)

        self.basic_info_fields.setColumnStretch(1, 1)

        self.basic_info_vlayout.addWidget(self.basic_info_label)
        self.basic_info_vlayout.addLayout(self.basic_info_fields)

        # Pricing Section
        self.pricing_frame = QFrame(self)
        self.pricing_frame.setStyleSheet("background-color: #d8f3dc; border-radius: 8px; padding: 10px;")
        self.pricing_vlayout = QVBoxLayout(self.pricing_frame)

        self.pricing_label = QLabel("Pricing Information")
        self.pricing_label.setStyleSheet("font-weight: bold; color: #2d6a4f;")
        self.pricing_vlayout.addWidget(self.pricing_label)

        self.pricing_fields = QGridLayout()

        self.selling_price_label = QLabel("Selling Price:")
        self.selling_price_label.setFixedWidth(label_width)
        self.selling_price_input = QLineEdit()
        self.selling_price_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d{1,2})?$")))

        self.mrp_label = QLabel("MRP:")
        self.mrp_label.setFixedWidth(label_width)
        self.mrp_input = QLineEdit()
        self.mrp_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d{1,2})?$")))

        self.cost_price_label = QLabel("Cost Price:")
        self.cost_price_label.setFixedWidth(label_width)
        self.cost_price_input = QLineEdit()
        self.cost_price_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d{1,2})?$")))

        self.pricing_fields.addWidget(self.selling_price_label, 0, 0)
        self.pricing_fields.addWidget(self.selling_price_input, 0, 1)
        self.pricing_fields.addWidget(self.mrp_label, 1, 0)
        self.pricing_fields.addWidget(self.mrp_input, 1, 1)
        self.pricing_fields.addWidget(self.cost_price_label, 2, 0)
        self.pricing_fields.addWidget(self.cost_price_input, 2, 1)

        self.pricing_fields.setColumnStretch(1, 1)
        self.pricing_vlayout.addLayout(self.pricing_fields)

        # Stock Information Section
        self.stock_frame = QFrame(self)
        self.stock_frame.setStyleSheet("background-color: #f9dcc4; border-radius: 8px; padding: 10px;")
        self.stock_vlayout = QVBoxLayout(self.stock_frame)

        self.stock_label = QLabel("Stock Information")
        self.stock_label.setStyleSheet("font-weight: bold; color: #a66a00;")
        self.stock_vlayout.addWidget(self.stock_label)

        self.stock_fields = QGridLayout()

        self.opening_stock_label = QLabel("Opening Stock:")
        self.opening_stock_label.setFixedWidth(label_width)
        self.opening_stock_input = QLineEdit()
        self.opening_stock_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d{1,3})?$")))

        self.reorder_point_label = QLabel("Reorder Point:")
        self.reorder_point_label.setFixedWidth(label_width)
        self.reorder_point_input = QLineEdit()
        self.reorder_point_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d{1,3})?$")))

        self.stock_fields.addWidget(self.opening_stock_label, 0, 0)
        self.stock_fields.addWidget(self.opening_stock_input, 0, 1)
        self.stock_fields.addWidget(self.reorder_point_label, 1, 0)
        self.stock_fields.addWidget(self.reorder_point_input, 1, 1)

        self.stock_fields.setColumnStretch(1, 1)
        self.stock_vlayout.addLayout(self.stock_fields)

        # Buttons
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.add_item_to_database)

        self.cancel_button = QPushButton("Cancel")

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(self.new_item_label)
        layout.addWidget(self.basic_info_frame)
        layout.addWidget(self.pricing_frame)
        layout.addWidget(self.stock_frame)
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def add_item_to_database(self):
            db = Database()
            errorString = ""
            is_name_unique = db.is_name_unique(self.name_input.text())
            name_text = self.name_input.text()
            is_gtin_unique = db.is_gtin_unique(self.gstn_input.text())
            gtin_text = self.gstn_input.text()
            if not is_name_unique:
                 errorString += f"{name_text} is already in the database. \n"

            if not is_gtin_unique:
                 errorString += f"{gtin_text} is already in the database. \n"

                

            
                
        

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

        # Layout for Inventory list
        self.inventory_layout = QVBoxLayout(self.inventory_list)
        self.inventory_layout.setContentsMargins(0 ,0 ,0 ,0)
        self.inventory_layout.setSpacing(0)

        #inventory list top bar
        self.inventory_list_topbar = QFrame(self.inventory_list)
        self.inventory_list_topbar.setObjectName("inventory_list_topbar")

        
        #inventory list top bar layout
        self.inventory_list_topbar_layout = QHBoxLayout(self.inventory_list_topbar)
        self.inventory_list_topbar_layout.setContentsMargins(5, 5, 5, 5)
        self.inventory_list_topbar_layout.setSpacing(5)

        #inventory list top bar search
        self.inventory_list_search = QLineEdit(self.inventory_list_topbar)
        self.inventory_list_search.setObjectName("inventory_list_search")
        self.inventory_list_search.setPlaceholderText("Search Inventory")

        #self.inventory_list_search.textChanged.connect(self.search_inventory)

        #inventory list top bar add new
        self.inventory_list_addnew = QPushButton("Add New", self.inventory_list_topbar)
        self.inventory_list_addnew.setObjectName("inventory_list_addnew")

        #self.inventory_list_addnew.clicked.connect(self.add_new_inventory)

        self.inventory_list_topbar_layout.addWidget(self.inventory_list_search)
        self.inventory_list_topbar_layout.addWidget(self.inventory_list_addnew)

        self.inventory_layout.addWidget(self.inventory_list_topbar)
        self.inventory_layout.addStretch()

        # Layout for Inventory Info
        self.inventory_info.addWidget(AddNewInventoryPanel(self))
        self.inventory_info.setCurrentIndex(0)

        self.layout.addWidget(self.inventory_list)
        self.layout.addWidget(self.inventory_info)

