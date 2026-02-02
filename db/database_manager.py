import sqlite3

class DatabaseManager:
    def __init__(self, db_path="program.db"):
        self.db_path = db_path
        self._init_db()

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def execute(self, sql, params=()):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur

    def fetchall(self, cursor):
        return cursor.fetchall()

    def _init_db(self):
        with self.connect() as conn:

            # -----------------------------
            # paper_formats
            # -----------------------------
            conn.execute("""
                CREATE TABLE IF NOT EXISTS paper_formats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    width_mm REAL NOT NULL,
                    height_mm REAL NOT NULL
                );
            """)

            # -----------------------------
            # ShippingLabelType_definitions
            # -----------------------------
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ShippingLabelType_definitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    carrier TEXT NOT NULL,
                    label_type TEXT NOT NULL,
                    keywords TEXT NOT NULL,
                    format_id INTEGER NOT NULL,
                    FOREIGN KEY(format_id) REFERENCES paper_formats(id)
                );
            """)

            # -----------------------------
            # crop_data
            # -----------------------------
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crop_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_label_id INTEGER NOT NULL,
                    paper_format_id INTEGER NOT NULL,
                    crop_x0 REAL NOT NULL,
                    crop_y0 REAL NOT NULL,
                    crop_x1 REAL NOT NULL,
                    crop_y1 REAL NOT NULL,
                    rotation INTEGER NOT NULL DEFAULT 0,
                    UNIQUE (supplier_label_id, paper_format_id),
                    FOREIGN KEY(supplier_label_id) REFERENCES ShippingLabelType_definitions(id),
                    FOREIGN KEY(paper_format_id) REFERENCES paper_formats(id)
                );
            """)