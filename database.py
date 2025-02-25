import mysql.connector

class Database:
    def __init__(self):
        """Initialize database connection and create database/tables if needed."""
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",      # Change this
            password="Bhavya7645@"   # Change this
        )
        self.cursor = self.conn.cursor()
        
        # Ensure database exists
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS storeflow")
        self.conn.database = "storeflow"  # Switch to our database

        # Ensure items table exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                price DECIMAL(10,2) DEFAULT 0.00,
                discount DECIMAL(10,2) DEFAULT 0.00,
                stock INT DEFAULT 0
            )
        """)

        self.conn.commit()

    def fetch_items(self, search_query=""):
        """Fetch items matching the search query."""
        self.cursor.execute("SELECT * FROM items WHERE name LIKE %s LIMIT 20", (f"%{search_query}%",))
        return self.cursor.fetchall()

    def add_item(self, name, price, discount, stock):
        """Add a new item to the database."""
        try:
            self.cursor.execute("INSERT INTO items (name, price, discount, stock) VALUES (%s, %s, %s, %s)",
                                (name, price, discount, stock))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error adding item: {e}")

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
