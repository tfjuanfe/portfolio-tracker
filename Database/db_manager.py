import sqlite3
import hashlib

class Database_Manager:
    def __init__(self):
        self.db_name = "database.db"
        self.create_tables()

    def create_tables(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                value REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                ticker TEXT NOT NULL,
                target_price REAL NOT NULL,
                condition TEXT NOT NULL,
                active INTEGER DEFAULT 1
            )
        """)

        connection.commit()
        connection.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            hashed = self.hash_password(password)
            cursor.execute("INSERT INTO users (username, password) VALUES (?,?)",
                           (username, hashed))
            connection.commit()
            connection.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        hashed = self.hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                      (username, hashed))
        user = cursor.fetchone()
        connection.close()
        return user is not None

    def add_asset(self, username, asset_name, asset_type, value):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO assets (username, asset_name, asset_type, value) VALUES (?, ?, ?, ?)",
                      (username, asset_name, asset_type, value))
        connection.commit()
        connection.close()

    def get_assets(self, username):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM assets WHERE username = ?", (username,))
        assets = cursor.fetchall()
        connection.close()
        return assets

    def delete_asset(self, asset_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
        connection.commit()
        connection.close()

    def modify_asset(self, asset_id, new_name, new_value):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE assets SET asset_name = ?, value = ? WHERE id = ?",
                      (new_name, new_value, asset_id))
        connection.commit()
        connection.close()

    def add_alert(self, username, ticker, target_price, condition):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO alerts (username, ticker, target_price, condition) VALUES (?,?,?,?)",
            (username, ticker, target_price, condition)
        )
        connection.commit()
        connection.close()

    def get_alerts(self, username):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM alerts WHERE username = ? AND active = 1", (username,))
        alerts = cursor.fetchall()
        connection.close()
        return alerts

    def delete_alert(self, alert_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
        connection.commit()
        connection.close()