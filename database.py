from PyQt6.QtSql import QSqlDatabase, QSqlQuery

class Database:
    def __init__(self):
        """Initialize database connection and create database/tables if needed."""
        self.db = QSqlDatabase.addDatabase("QMYSQL")  # Use QSqlDatabase
        self.db.setHostName("localhost")
        self.db.setUserName("root")
        self.db.setPassword("Bhavya7645@")
        self.db.setDatabaseName("storeflow")

        if not self.db.open():
            print(f"❌ Database connection failed: {self.db.lastError().text()}")
            return

        print("✅ Database connection established.")
        
        db = QSqlDatabase.database()
        print("Database driver in use:", db.driverName())

        self.create_table()

    def create_table(self):
        """Creates inventory table if it doesn't exist."""
        query = QSqlQuery()
        query.exec("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE, 
                gtin CHAR(13) NOT NULL UNIQUE,
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

    def is_name_unique(self, name):
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

