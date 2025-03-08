import mysql.connector

import mysql.connector

class Database:
    def __init__(self):
        """Initialize database connection and create database/tables if needed."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Change this
                password="Bhavya7645@"  # Change this
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

    def add_item(self, name, gtin, unit, selling_price, mrp, cost_price, opening_stock, reorder_point):
        """Adds new Item to the Inventory"""
        try:
            query = """
                INSERT INTO inventory (name, gtin, unit_of_measurement, selling_price, mrp, cost_price, stock, reorder_point) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, gtin, unit, selling_price, mrp, cost_price, opening_stock, reorder_point)
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"✅ Item '{name}' added successfully!")
        except mysql.connector.IntegrityError as e:
            print(f"❌ Error: {e}")  # Handles duplicate name/GTIN errors
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


# Initialize the database
db = Database()
print("Database and table initialized successfully!")

db.add_item("cheese","1234567891234","kg",50,50,40,20,10)


