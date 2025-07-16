import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/results.db')

def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY,
                test_name TEXT,
                result TEXT,
                measurement REAL,
                timestamp DATETIME
            )
        ''')

def log_test_result(test_name, result_bool, measurement=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO test_results (test_name, result, measurement, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (test_name, 'PASS' if result_bool else 'FAIL', measurement, datetime.now().isoformat()))

def fetch_test_results():
    import sqlite3
    DB_PATH = os.path.join(os.path.dirname(__file__), '../db/results.db')
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('SELECT test_name, result, measurement, timestamp FROM test_results')
        return cursor.fetchall()

def clear_test_results():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM test_results')
