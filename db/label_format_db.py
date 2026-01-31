from .database_manager import DatabaseManager
from .models import LabelFormat

class LabelFormatDB:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add(self, name, width_mm, height_mm):
        with self.db.connect() as conn:
            conn.execute("""
                INSERT INTO label_formats (name, width_mm, height_mm)
                VALUES (?, ?, ?)
            """, (name, width_mm, height_mm))