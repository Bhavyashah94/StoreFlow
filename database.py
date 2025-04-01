from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import Qt

class Database:
    def __init__(self):
        """Ensure database exists and establish connection."""
        self.ensure_database()

        # Initialize connection
        self.db = QSqlDatabase.addDatabase("QMYSQL")
        self.db.setHostName("localhost")
        self.db.setUserName("root")
        self.db.setPassword("Bhavya7645@")
        self.db.setDatabaseName("storeflow")

        if not self.db.open():
            print(f"❌ Database connection failed: {self.db.lastError().text()}")
            return

        print("✅ Database connection established.")
        print("Database driver in use:", self.db.driverName())

        self.create_table()

    def ensure_database(self):
        """Ensures the 'storeflow' database exists before connecting."""
        temp_db = QSqlDatabase.addDatabase("QMYSQL", "TempConnection")
        temp_db.setHostName("localhost")
        temp_db.setUserName("root")
        temp_db.setPassword("Bhavya7645@")

        if not temp_db.open():
            print(f"❌ Cannot connect to MySQL server: {temp_db.lastError().text()}")
            return
        
        query = QSqlQuery(temp_db)
        query.exec("CREATE DATABASE IF NOT EXISTS storeflow")

        temp_db.close()
        QSqlDatabase.removeDatabase("TempConnection")

    def create_table(self):
        """Creates inventory and transactions tables with payment details."""
        query = QSqlQuery()

        # Inventory table (unchanged)
        query.exec("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE, 
                gtin CHAR(13) UNIQUE,
                unit_of_measurement VARCHAR(50),
                selling_price DECIMAL(10,2) CHECK (selling_price >= 0),
                mrp DECIMAL(10,2) CHECK (mrp >= 0),
                cost_price DECIMAL(10,2) CHECK (cost_price >= 0),
                stock DECIMAL(10,3),
                reorder_point DECIMAL(10,3) CHECK (reorder_point >= 0)
            )
        """)

        # Transactions table with payment details
        query.exec("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                inventory_id INT NOT NULL,
                inventory_name VARCHAR(255) NOT NULL,  -- Store item name for easy reference
                transaction_type ENUM('sale', 'purchase', 'adjustment') NOT NULL,
                quantity DECIMAL(10,3) CHECK (quantity >= 0),
                price DECIMAL(10,2) CHECK (price >= 0),
                discount DECIMAL(10,2) CHECK (discount >= 0),
                payment_mode ENUM('cash', 'credit', 'UPI', 'other') NOT NULL,
                cash_received DECIMAL(10,2) DEFAULT NULL,
                return_amount DECIMAL(10,2) DEFAULT NULL,
                reference_no VARCHAR(255) DEFAULT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (inventory_id) REFERENCES inventory(id) ON DELETE CASCADE
            )
        """)


        if query.lastError().isValid():
            print(f"❌ Table creation error: {query.lastError().text()}")
        else:
            print("✅ Database and tables initialized successfully.")

    def add_item(self, name, gtin, unit, selling_price, mrp, cost_price, stock, reorder_point):
        """Adds a new item to the inventory."""
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO inventory (name, gtin, unit_of_measurement, selling_price, mrp, cost_price, stock, reorder_point)
            VALUES (:name, :gtin, :unit, :selling_price, :mrp, :cost_price, :stock, :reorder_point)
        """)
        query.bindValue(":name", name)
        query.bindValue(":gtin", gtin)
        query.bindValue(":unit", unit)
        query.bindValue(":selling_price", selling_price)
        query.bindValue(":mrp", mrp)
        query.bindValue(":cost_price", cost_price)
        query.bindValue(":stock", stock)
        query.bindValue(":reorder_point", reorder_point)

        if not query.exec():
            print(f"❌ Insert error: {query.lastError().text()}")
            return False
        
        print(f"✅ Item '{name}' added successfully!")
        return True
    
    def delete_item(self, name: str) -> bool:
        """Deletes an item from inventory."""
        query = QSqlQuery()
        query.prepare("DELETE FROM inventory WHERE name = :name")
        query.bindValue(":name", name)

        if not query.exec():
            print(f"❌ Query error: {query.lastError().text()}")
            return False

        if query.numRowsAffected() > 0:
            return True  # Item was successfully deleted

        print("⚠️ No item deleted (Item may not exist)")
        return False  # Item didn't exist or was not deleted


    def is_name_unique(self, name: str) -> bool:
        """Checks if an item name is unique in the inventory."""
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM inventory WHERE name = :name")
        query.bindValue(":name", name)

        if not query.exec():
            print(f"❌ Query error: {query.lastError().text()}")
            return False

        if query.next():
            return query.value(0) == 0  # True if name is unique

        return False
    
    def is_gtin_unique(self, gtin: str) -> bool:
        """Checks if an item EAN is unique in the inventory."""
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM inventory WHERE gtin = :gtin")
        query.bindValue(":gtin", gtin)

        if not query.exec():
            print(f"❌ Query error: {query.lastError().text()}")
            return False

        if query.next():
            return query.value(0) == 0  # True if gtin is unique

        return False
    
    def get_inventory_items(self, search_query=""):
        """Fetch inventory items from the database, optionally filtering by search_query."""
        query = QSqlQuery()

        if search_query:
            query.prepare("""
                SELECT id, name, gtin, unit_of_measurement, selling_price, mrp, cost_price, stock, reorder_point 
                FROM inventory 
                WHERE name LIKE :search_query OR gtin LIKE :search_query
            """)
            query.bindValue(":search_query", f"%{search_query}%")
        else:
            query.prepare("SELECT id, name, gtin, unit_of_measurement, selling_price, mrp, cost_price, stock, reorder_point FROM inventory")

        query.exec()

        inventory_items = []
        while query.next():
            item = {
                "id": query.value(0),
                "name": query.value(1),
                "gtin": query.value(2),
                "unit": query.value(3),
                "selling_price": query.value(4),
                "mrp": query.value(5),
                "cost_price": query.value(6),
                "stock": query.value(7),
                "reorder_point": query.value(8),
            }
            inventory_items.append(item)

        return inventory_items

    def record_transaction(self, inventory_name, transaction_type, quantity, price, discount=0.00, 
                        payment_mode="cash", cash_received=None, return_amount=None, reference_no=None, timestamp=None):
        """Records a transaction using inventory name instead of ID."""
        
        # Fetch inventory ID using inventory name
        query = QSqlQuery()
        query.prepare("SELECT id FROM inventory WHERE name = :inventory_name")
        query.bindValue(":inventory_name", inventory_name)

        if not query.exec() or not query.next():
            print(f"❌ Inventory item '{inventory_name}' not found.")
            return False

        inventory_id = query.value(0)

        if not self.update_stock(inventory_id, quantity, transaction_type):
            return False  # Stock update failed

        query.prepare("""
            INSERT INTO transactions (inventory_name, inventory_id, transaction_type, quantity, price, discount, 
                                    payment_mode, cash_received, return_amount, reference_no, timestamp)
            VALUES (:inventory_name, :inventory_id, :transaction_type, :quantity, :price, :discount, 
                    :payment_mode, :cash_received, :return_amount, :reference_no, :timestamp)
        """)
        query.bindValue(":inventory_name", inventory_name)
        query.bindValue(":inventory_id", inventory_id)
        query.bindValue(":transaction_type", transaction_type)
        query.bindValue(":quantity", quantity)
        query.bindValue(":price", price)
        query.bindValue(":discount", discount)
        query.bindValue(":payment_mode", payment_mode)

        # Handle payment fields
        if payment_mode == "cash":
            query.bindValue(":cash_received", cash_received if cash_received is not None else 0.00)
            query.bindValue(":return_amount", return_amount if return_amount is not None else 0.00)
            query.bindValue(":reference_no", None)
        else:  # UPI or credit
            query.bindValue(":cash_received", None)
            query.bindValue(":return_amount", None)
            query.bindValue(":reference_no", reference_no)

        # Bind timestamp
        query.bindValue(":timestamp", timestamp)

        if not query.exec():
            print(f"❌ Transaction error: {query.lastError().text()}")
            return False

        print(f"✅ Transaction recorded for '{inventory_name}' with payment mode {payment_mode}.")
        return True



    def get_transactions(self, inventory_name=None):
        """Fetch transactions based on inventory name."""
        query = QSqlQuery()

        if inventory_name:
            query.prepare("""
                SELECT id, inventory_name, inventory_id, transaction_type, quantity, price, discount, payment_mode, cash_received, return_amount, reference_no, timestamp 
                FROM transactions WHERE inventory_name = :inventory_name ORDER BY timestamp DESC
            """)
            query.bindValue(":inventory_name", inventory_name)
        else:
            query.prepare("""
                SELECT id, inventory_name, inventory_id, transaction_type, quantity, price, discount, payment_mode, cash_received, return_amount, reference_no, timestamp 
                FROM transactions ORDER BY timestamp DESC
            """)

        query.exec()

        transactions = []
        while query.next():
            transaction = {
                "id": query.value(0),
                "inventory_name": query.value(1),  # No need to fetch separately
                "inventory_id": query.value(2),  # Still available if needed
                "transaction_type": query.value(3),
                "quantity": query.value(4),
                "price": query.value(5),
                "discount": query.value(6),
                "payment_mode": query.value(7),
                "cash_received": query.value(8),
                "return_amount": query.value(9),
                "reference_no": query.value(10),
                "timestamp": query.value(11),
            }
            transactions.append(transaction)

        return transactions

    def update_stock(self, inventory_id, quantity, transaction_type):
        """Updates stock quantity based on transaction type (sale or restock)."""
        query = QSqlQuery()

        # Determine stock adjustment (subtract for sale, add for restock)
        if transaction_type == "sale":
            query.prepare("UPDATE inventory SET stock = stock - :quantity WHERE id = :inventory_id")
        elif transaction_type == "restock":
            query.prepare("UPDATE inventory SET stock = stock + :quantity WHERE id = :inventory_id")
        else:
            print(f"⚠️ Unknown transaction type: {transaction_type}")
            return False

        query.bindValue(":quantity", quantity)
        query.bindValue(":inventory_id", inventory_id)

        if not query.exec():
            print(f"❌ Stock update failed: {query.lastError().text()}")
            return False

        print(f"✅ Stock updated for inventory ID {inventory_id}.")
        return True

    def has_transactions(self, inventory_name: str) -> bool:
        """Returns True if the specified inventory item has transactions."""
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM transactions WHERE inventory_name = :inventory_name")
        query.bindValue(":inventory_name", inventory_name)

        if not query.exec():
            print(f"❌ Query error: {query.lastError().text()}")
            return False  # Assume no transactions if query fails

        if query.next():
            return query.value(0) > 0  # Check if count > 0

        return False
    
    def update_item(self, name, unit, selling_price, mrp, cost_price, stock, reorder_point):
        """Updates an inventory item based on its unique name."""
        query = QSqlQuery()
        query.prepare("""
            UPDATE inventory 
            SET unit_of_measurement = :unit, selling_price = :selling_price, mrp = :mrp, 
                cost_price = :cost_price, stock = :stock, reorder_point = :reorder_point
            WHERE name = :name
        """)
        query.bindValue(":name", name)
        query.bindValue(":unit", unit)
        query.bindValue(":selling_price", selling_price)
        query.bindValue(":mrp", mrp)
        query.bindValue(":cost_price", cost_price)
        query.bindValue(":stock", stock)
        query.bindValue(":reorder_point", reorder_point)

        if query.exec():
            return True
        else:
            print("Inventory update failed:", query.lastError().text())
            return False

    def record_edit_transaction(self, inventory_name, changes):
        """Logs an inventory edit as a transaction with change details in reference_no."""
        # Fetch inventory ID using inventory name
        query = QSqlQuery()
        query.prepare("SELECT id FROM inventory WHERE name = :inventory_name")
        query.bindValue(":inventory_name", inventory_name)

        if not query.exec() or not query.next():
            print(f"❌ Inventory item '{inventory_name}' not found.")
            return False

        inventory_id = query.value(0)

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO transactions (inventory_name, inventory_id, transaction_type, quantity, price, discount, 
                                    payment_mode, reference_no)
            VALUES (:inventory_name, :inventory_id, 'adjustment', 0, 0, 0, 'other', :reference_no)
        """)
        query.bindValue(":inventory_name", inventory_name)
        query.bindValue(":inventory_id", inventory_id)
        query.bindValue(":reference_no", changes)  # Storing changes as a string
        print(query)

        if not query.exec():
            print("Transaction log failed:", query.lastError().text())