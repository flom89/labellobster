import sqlite3

class DatabaseManager:
    def __init__(self, db_path="label_formats.db"):
        self.db_path = db_path
        self._init_db()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS label_formats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    width_mm REAL NOT NULL,
                    height_mm REAL NOT NULL
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS label_crops (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    pdf_width REAL NOT NULL,
                    pdf_height REAL NOT NULL,
                    crop_x0 REAL NOT NULL,
                    crop_y0 REAL NOT NULL,
                    crop_x1 REAL NOT NULL,
                    crop_y1 REAL NOT NULL,
                    rotation INTEGER NOT NULL DEFAULT 90,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)