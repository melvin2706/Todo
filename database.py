# Module for database connection (creation of our instance for database connectivity)
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return conn