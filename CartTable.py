from PyQt6.QtWidgets import QLineEdit, QStyledItemDelegate, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QWidget
from PyQt6.QtCore import Qt


class CartTable(QWidget):
    def __init__(self, store_ui):
        super().__init__()
        self.store_ui = store_ui  # Reference to StoreFlowUI
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Cart Table
        self.table = QTableWidget(0, 6)  # Extra column for row numbering
        self.table.setHorizontalHeaderLabels(["NO", "Item Name", "Quantity", "Price", "Discount", "Total"])

        # Hide vertical header
        self.table.verticalHeader().setVisible(False)

        # Column Sizing
        self.table.setColumnWidth(0, 50)  # Row number
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # "Item Name"
        for i in range(2, 6):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(i, 100)

        # Disable editing for non-editable columns
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.layout.addWidget(self.table)

        # Add first row with QLineEdit
        self.add_empty_row()

    def update_row_numbers(self):
        """Updates the numbering in the first column after adding/removing rows."""
        for row in range(self.table.rowCount()):
            item = QTableWidgetItem(str(row + 1))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item)

    def add_empty_row(self):
        """Adds an empty row and inserts a QLineEdit in the 'Item Name' column."""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # Update row numbers
        self.update_row_numbers()

        # Add QLineEdit in the 'Item Name' column
        name_edit = QLineEdit(self)
        name_edit.setPlaceholderText("Search for an item...")
        self.table.setCellWidget(row_count, 1, name_edit)

        # Connect signal to show popup
        name_edit.textEdited.connect(lambda: self.show_add_item_popup(name_edit))

    def show_add_item_popup(self, name_edit):
        """Shows the Add Item popup when typing in the name field."""
        self.store_ui.toggle_overlay(True)  # Show overlay
        self.store_ui.overlayClicked.connect(self.close_popup)

        # Set popup position just below the top bar
        margin_top = 60  # Adjust based on top bar height
        screen_width = self.store_ui.width()
        
        self.popup = QWidget(self)

        self.popupSearchBar = QLineEdit()
        self.popupSearchBar.setText(name_edit.text())
        name_edit.clear()

        self.popupTable = QTableWidget(1, 4)
        self.popupTable.setHorizontalHeaderLabels(["Item Name", "GTIN", "Quantity", "Price"])

        self.popupTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.popupTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.popupTable.setColumnWidth(1, 200)

        for i in range(2, 4):
            self.popupTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            self.popupTable.setColumnWidth(i, 100)

        popup_width = 800
        popup_height = 600
        popup_x = (screen_width - popup_width) // 2  # Center horizontally
        popup_y = margin_top  # Position below the top bar

        self.popupLayout = QVBoxLayout(self.popup)
        self.popupLayout.addWidget(self.popupSearchBar)
        self.popupLayout.addWidget(self.popupTable)

        self.popup.setGeometry(popup_x, popup_y, popup_width, popup_height)
        self.popup.setStyleSheet("background-color: white; border-radius: 10px; color:  black;")
        
        self.popup.setParent(self.store_ui)  # Ensure it belongs to main window
        self.popup.setWindowFlags(Qt.WindowType.Popup)  # Helps with stacking
        self.popup.show()
        self.popupSearchBar.setFocus()
        self.popup.raise_()  # 🔥 Ensure it's above the overlay



    def close_popup(self):
        """Closes the popup and hides the overlay."""
        if hasattr(self, "popup"):
            self.popup.close()
            del self.popup
            self.store_ui.toggle_overlay(False)  # Hide overlay

    def remove_selected_item(self):
        """Removes the selected row and updates numbering."""
        selected_rows = {index.row() for index in self.table.selectedIndexes()}
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
        self.update_row_numbers()

        # If table is empty, add a new QLineEdit in the first row
        if self.table.rowCount() == 0:
            self.add_empty_row()
