import mysql.connector

class Database:
    def __init__(self):
        """Initialize database connection and create database/tables if needed."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Change this
                password="Ohio6969"  # Change this
            )
            self.cursor = self.conn.cursor()
            print("✅ Database connection established.")

            # Ensure database exists
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS storeflow")
            self.conn.database = "storeflow"  # Switch to our database

            # Ensure inventory table exists
            self.cursor.execute("""
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

            self.conn.commit()
            print("✅ Database and table initialized successfully.")

        except mysql.connector.Error as e:
            print(f"❌ Database connection failed: {e}")
            self.conn = None  # Ensure connection object doesn't exist if failed

    def add_item(
        self, 
        name: str, 
        gtin: str, 
        unit: str, 
        selling_price: float, 
        mrp: float, 
        cost_price: float, 
        stock: float, 
        reorder_point: float
    ) -> bool:
        """Adds a new item to the inventory."""
        if not self.conn:
            print("❌ Error: No database connection.")
            return False

        try:
            query = """
                INSERT INTO inventory (name, gtin, unit_of_measurement, selling_price, mrp, cost_price, stock, reorder_point) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, gtin, unit, selling_price, mrp, cost_price, stock, reorder_point)
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"✅ Item '{name}' added successfully!")
            return True  # Success
        except mysql.connector.IntegrityError as e:
            print(f"❌ Integrity Error: {e}")  # Handles duplicate name/GTIN errors
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return False

# Initialize database and add a test item
db = Database()
db.add_item("Wheat Flour", "1234567890123", "kg", 50.00, 55.00, 40.00, 100.500, 10.000)



