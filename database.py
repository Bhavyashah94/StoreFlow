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
        """Creates inventory table if it doesn't exist."""
        query = QSqlQuery()
        query.exec("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE, 
                gtin CHAR(13) UNIQUE,
                unit_of_measurement VARCHAR(50),
                selling_price DECIMAL(10,2) CHECK (selling_price >= 0),
                mrp DECIMAL(10,2) CHECK (mrp >= 0),
                cost_price DECIMAL(10,2) CHECK (cost_price >= 0),
                stock DECIMAL(10,3) CHECK (stock >= 0),
                reorder_point DECIMAL(10,3) CHECK (reorder_point >= 0)
            )
        """)

        if query.lastError().isValid():
            print(f"❌ Table creation error: {query.lastError().text()}")
        else:
            print("✅ Database and table initialized successfully.")

    def get_sales_summary(self):
        """Fetch latest sales summary from database"""
        query = QSqlQuery()
        query.exec("SELECT sub_total, tax, discount, round_off, total FROM sales_summary ORDER BY id DESC LIMIT 1")

        if query.next():
            return {
                "sub_total": query.value(0),
                "tax": query.value(1),
                "discount": query.value(2),
                "round_off": query.value(3),
                "total": query.value(4),
            }
        
        return None  # Fixed indentation issue

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
