from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                            QLabel, QLineEdit, QFormLayout, QStackedWidget, QGridLayout, QComboBox,
                            QProgressDialog, QMessageBox, QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt, QRegularExpression, QThread, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QRegularExpressionValidator
from database import Database
from inventoryItemWidget import InventoryItemWidget



class AddNewInventoryPanel(QWidget):
    item_added = pyqtSignal()
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
        self.name_input.setMaxLength(255)

        self.gtin_label = QLabel("GITN Number:")
        self.gtin_label.setFixedWidth(label_width)
        self.gtin_input = QLineEdit()
        self.gtin_input.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]{13}$")))
        self.gtin_input.setMaxLength(13)

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
        self.basic_info_fields.addWidget(self.gtin_label, 1, 0)
        self.basic_info_fields.addWidget(self.gtin_input, 1, 1)
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
        name = self.name_input.text().strip()
        gtin = self.gtin_input.text().strip()
        unit = self.unit_input.currentText()
        selling_price = self.selling_price_input.text().strip()
        mrp = self.mrp_input.text().strip()
        cost_price = self.cost_price_input.text().strip()
        opening_stock = self.opening_stock_input.text().strip() or "0"
        reorder_point = self.reorder_point_input.text().strip() or "0"

        # Validate required fields
        if not name or not unit:
            QMessageBox.warning(self, "Input Error", "Name and Unit of Measurement are required!")
            return

        if not mrp or not cost_price:
            QMessageBox.warning(self, "Input Error", "MRP and Cost Price are required!")
            return

        # Validate GTIN: If not empty, it must be exactly 13 digits
        if gtin and (not gtin.isdigit() or len(gtin) != 13):
            QMessageBox.warning(self, "Input Error", "GTIN must be exactly 13 digits or left empty!")
            return

        db = Database()
        
        if not db.is_name_unique(name):
            QMessageBox.warning(self, "Duplicate Error", "An item with this name already exists!")
            return
        
        if gtin and not db.is_gtin_unique(gtin):
            QMessageBox.warning(self, "Duplicate Error", "An item with this GTIN number already exists!")
            return

        # Convert numeric values safely
        try:
            mrp = float(mrp)
            cost_price = float(cost_price)
            selling_price = float(selling_price) if selling_price else mrp  # Default selling price to MRP
            opening_stock = float(opening_stock)
            reorder_point = float(reorder_point)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for pricing and stock fields!")
            return

        # Insert into database
        success = db.add_item(name, gtin if gtin else None, unit, selling_price, mrp, cost_price, opening_stock, reorder_point)
        
        if success:
            QMessageBox.information(self, "Success", "Item added successfully!")
            self.clear_fields()
            self.item_added.emit()
            
        else:
            QMessageBox.critical(self, "Database Error", "Failed to add the item. Please try again!")

    def clear_fields(self):
        self.name_input.clear()
        self.gtin_input.clear()
        self.unit_input.setCurrentIndex(-1)  # Reset combo box
        self.selling_price_input.clear()
        self.mrp_input.clear()
        self.cost_price_input.clear()
        self.opening_stock_input.clear()
        self.reorder_point_input.clear()

class EditInventoryPanel(QWidget):
    item_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("edit_inventory_panel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 400, 10)
        layout.setSpacing(10)

        self.edit_item_label = QLabel("Edit Item")
        self.edit_item_label.setObjectName("edit_item_label")
        self.edit_item_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

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
        self.name_input.setDisabled(True)  # Disable the Name field
        self.name_input.setStyleSheet("color: gray;")  # Optional: Style it to look disabled

        self.gtin_label = QLabel("GTIN Number:")
        self.gtin_label.setFixedWidth(label_width)
        self.gtin_input = QLineEdit()
        self.gtin_input.setDisabled(True)  # Disable GTIN field
        self.gtin_input.setStyleSheet("color: gray;")  # Optional: Style it to look disabled

        self.unit_label = QLabel("Unit of Measurement:")
        self.unit_label.setFixedWidth(label_width)
        self.unit_input = QComboBox()
        self.unit_input.setEditable(False)
        self.unit_input.addItems(["Kg", "gms", "Pcs"])

        self.basic_info_fields.addWidget(self.name_label, 0, 0)
        self.basic_info_fields.addWidget(self.name_input, 0, 1)
        self.basic_info_fields.addWidget(self.gtin_label, 1, 0)
        self.basic_info_fields.addWidget(self.gtin_input, 1, 1)
        self.basic_info_fields.addWidget(self.unit_label, 2, 0)
        self.basic_info_fields.addWidget(self.unit_input, 2, 1)

        self.basic_info_vlayout.addWidget(self.basic_info_label)
        self.basic_info_vlayout.addLayout(self.basic_info_fields)

        # Pricing Section (Same as Add New Panel)
        self.pricing_frame = QFrame(self)
        self.pricing_frame.setStyleSheet("background-color: #d8f3dc; border-radius: 8px; padding: 10px;")
        self.pricing_vlayout = QVBoxLayout(self.pricing_frame)

        self.pricing_label = QLabel("Pricing Information")
        self.pricing_label.setStyleSheet("font-weight: bold; color: #2d6a4f;")

        self.selling_price_label = QLabel("Selling Price:")
        self.selling_price_input = QLineEdit()

        self.mrp_label = QLabel("MRP:")
        self.mrp_input = QLineEdit()

        self.cost_price_label = QLabel("Cost Price:")
        self.cost_price_input = QLineEdit()

        self.pricing_fields = QGridLayout()
        self.pricing_fields.addWidget(self.selling_price_label, 0, 0)
        self.pricing_fields.addWidget(self.selling_price_input, 0, 1)
        self.pricing_fields.addWidget(self.mrp_label, 1, 0)
        self.pricing_fields.addWidget(self.mrp_input, 1, 1)
        self.pricing_fields.addWidget(self.cost_price_label, 2, 0)
        self.pricing_fields.addWidget(self.cost_price_input, 2, 1)

        self.pricing_vlayout.addWidget(self.pricing_label)
        self.pricing_vlayout.addLayout(self.pricing_fields)

        # Stock Section (Same as Add New Panel)
        self.stock_frame = QFrame(self)
        self.stock_frame.setStyleSheet("background-color: #f9dcc4; border-radius: 8px; padding: 10px;")
        self.stock_vlayout = QVBoxLayout(self.stock_frame)

        self.stock_label = QLabel("Stock Information")
        self.stock_label.setStyleSheet("font-weight: bold; color: #a66a00;")

        self.opening_stock_label = QLabel("Stock:")
        self.opening_stock_input = QLineEdit()

        self.reorder_point_label = QLabel("Reorder Point:")
        self.reorder_point_input = QLineEdit()

        self.stock_fields = QGridLayout()
        self.stock_fields.addWidget(self.opening_stock_label, 0, 0)
        self.stock_fields.addWidget(self.opening_stock_input, 0, 1)
        self.stock_fields.addWidget(self.reorder_point_label, 1, 0)
        self.stock_fields.addWidget(self.reorder_point_input, 1, 1)

        self.stock_vlayout.addWidget(self.stock_label)
        self.stock_vlayout.addLayout(self.stock_fields)

        # Buttons
        button_layout = QHBoxLayout()

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_item_in_database)

        self.cancel_button = QPushButton("Cancel")

        button_layout.addStretch()
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(self.edit_item_label)
        layout.addWidget(self.basic_info_frame)
        layout.addWidget(self.pricing_frame)
        layout.addWidget(self.stock_frame)
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def load_item_data(self, item_data):
        """Loads an existing item's details into the form for editing."""
        self.name_input.setText(item_data["name"])
        self.gtin_input.setText(item_data["gtin"])
        self.unit_input.setCurrentText(item_data["unit"])
        self.selling_price_input.setText(str(item_data["selling_price"]))
        self.mrp_input.setText(str(item_data["mrp"]))
        self.cost_price_input.setText(str(item_data["cost_price"]))
        self.opening_stock_input.setText(str(item_data["stock"]))
        self.reorder_point_input.setText(str(item_data["reorder_point"]))

    def update_item_in_database(self):
        """Updates the item details in the database with new values and logs the changes."""
        name = self.name_input.text().strip()
        unit = self.unit_input.currentText()
        selling_price = self.selling_price_input.text().strip()
        mrp = self.mrp_input.text().strip()
        cost_price = self.cost_price_input.text().strip()
        opening_stock = self.opening_stock_input.text().strip()
        reorder_point = self.reorder_point_input.text().strip()

        # Validate required fields
        if not name or not unit:
            QMessageBox.warning(self, "Input Error", "Unit of Measurement is required!")
            return

        if not mrp or not cost_price:
            QMessageBox.warning(self, "Input Error", "MRP and Cost Price are required!")
            return

        # Convert numeric values safely
        try:
            mrp = float(mrp)
            cost_price = float(cost_price)
            selling_price = float(selling_price) if selling_price else mrp  # Default selling price to MRP
            opening_stock = float(opening_stock) if opening_stock else 0
            reorder_point = float(reorder_point) if reorder_point else 0
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for pricing and stock fields!")
            return

        db = Database()
        inventory_items = db.get_inventory_items(search_query=name)
        if inventory_items:  # Ensure the list is not empty
            old_item_data = inventory_items[0]  # Get the first (and likely only) result
            print(old_item_data)
            if unit != old_item_data["unit"]:
                # Proceed with update logic
                pass
        else:
            print("Item not found in inventory!")


        if not old_item_data:
            QMessageBox.critical(self, "Database Error", "Item not found in the database!")
            return

        # Compare old and new values to log changes
        changes = []
        if unit != old_item_data["unit"]:
            changes.append(f"Unit changed from {old_item_data['unit']} to {unit}")
        if selling_price != old_item_data["selling_price"]:
            changes.append(f"Selling Price changed from {old_item_data['selling_price']} to {selling_price}")
        if mrp != old_item_data["mrp"]:
            changes.append(f"MRP changed from {old_item_data['mrp']} to {mrp}")
        if cost_price != old_item_data["cost_price"]:
            changes.append(f"Cost Price changed from {old_item_data['cost_price']} to {cost_price}")
        if opening_stock != old_item_data["stock"]:
            changes.append(f"Stock adjusted from {old_item_data['stock']} to {opening_stock}")
        if reorder_point != old_item_data["reorder_point"]:
            changes.append(f"Reorder Point changed from {old_item_data['reorder_point']} to {reorder_point}")

        # Update the database
        success = db.update_item(name, unit, selling_price, mrp, cost_price, opening_stock, reorder_point)

        if success:
            QMessageBox.information(self, "Success", "Item updated successfully!")

            # Log changes in transactions
            if changes:
                changes = [str(change).strip() for change in changes if change]  # Remove None & spaces
                log_message = "; ".join(changes).encode("utf-8").decode("utf-8")  # Ensure clean formatting

                print(repr(log_message))  # Debug output
                db.record_edit_transaction(name, log_message)
                
            self.item_updated.emit()
        else:
            QMessageBox.critical(self, "Database Error", "Failed to update the item. Please try again!")



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
        self.inventory_list_topbar.setFixedHeight(50)

        
        #inventory list top bar layout
        self.inventory_list_topbar_layout = QHBoxLayout(self.inventory_list_topbar)
        self.inventory_list_topbar_layout.setContentsMargins(5, 5, 5, 5)
        self.inventory_list_topbar_layout.setSpacing(5)

        #inventory list top bar search
        self.inventory_list_search = QLineEdit(self.inventory_list_topbar)
        self.inventory_list_search.setObjectName("inventory_list_search")
        self.inventory_list_search.setPlaceholderText("Search Inventory")

        self.inventory_list_search.textChanged.connect(lambda: self.load_inventory_items(self.inventory_list_search.text().strip()))


        #self.inventory_list_search.textChanged.connect(self.search_inventory)

        #inventory list top bar add new
        self.inventory_list_addnew = QPushButton("Add New", self.inventory_list_topbar)
        self.inventory_list_addnew.setObjectName("inventory_list_addnew")
        self.inventory_list_addnew.clicked.connect(self.show_add_new_panel)

        #self.inventory_list_addnew.clicked.connect(self.add_new_inventory)

        self.inventory_list_topbar_layout.addWidget(self.inventory_list_search)
        self.inventory_list_topbar_layout.addWidget(self.inventory_list_addnew)

        self.inventory_layout.addWidget(self.inventory_list_topbar)

        #Edit inventory panel
        self.edit_inventory_panel = EditInventoryPanel(self)
        self.edit_inventory_panel.item_updated.connect(self.load_inventory_items, self.show_add_new_panel)
        self.inventory_info.addWidget(self.edit_inventory_panel)

        # Add New Inventory Panel to StackedWidget
        self.add_new_inventory_panel = AddNewInventoryPanel(self)
        self.add_new_inventory_panel.item_added.connect(self.load_inventory_items)
        self.inventory_info.addWidget(self.add_new_inventory_panel)

        self.layout.addWidget(self.inventory_list)
        self.layout.addWidget(self.inventory_info)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.inventory_items_container = QWidget()
        self.inventory_items_layout = QVBoxLayout(self.inventory_items_container)
        self.inventory_items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.inventory_items_container)

        self.inventory_layout.addWidget(self.scroll_area)

        self.load_inventory_items()

    def show_add_new_panel(self):
        self.inventory_info.setCurrentWidget(self.add_new_inventory_panel)

    def show_edit_panel(self, item_data):
        self.edit_inventory_panel.load_item_data(item_data)
        self.inventory_info.setCurrentWidget(self.edit_inventory_panel)

    def load_inventory_items(self, search_query=""):
        """Loads inventory items into the UI with search filtering."""
        db = Database()
        items = db.get_inventory_items(search_query)
        print(items)

        # Clear existing widgets
        while self.inventory_items_layout.count():
            item = self.inventory_items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new items
        for item in items:
            item_widget = InventoryItemWidget(item)
            item_widget.right_clicked.connect(self.handle_right_click)
            item_widget.double_clicked.connect(self.handle_double_click)
            self.inventory_items_layout.addWidget(item_widget)


    def handle_right_click(self, action_data):
        """Handles right-click actions."""
        action, item_data = action_data

        if action == "edit":
            #QMessageBox.information(self, "Edit Item", f"Editing {item_data['name']}")
            # Open edit form here
            self.show_edit_panel(item_data)
        elif action == "delete":
            confirm = QMessageBox.question(self, "Delete Item", f"Are you sure you want to delete {item_data['name']}?")
            if confirm == QMessageBox.StandardButton.Yes:
                db = Database()
                db.delete_item(item_data['name'])
                self.load_inventory_items()  # Reload after deletion
        elif action == "details":
            QMessageBox.information(self, "Item Details", f"Showing details for {item_data['name']}")

    def handle_double_click(self, item_data):
        """Handles double-click actions."""
        QMessageBox.information(self, "Item Selected", f"You double-clicked on {item_data['name']}")



    def search_inventory(self):
        """Filters inventory based on user input."""
        search_text = self.inventory_list_search.text().strip()
        self.load_inventory_items(search_text)  # Reload list with search filter
        

