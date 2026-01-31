from .database_manager import DatabaseManager
from .models import LabelCrop

class LabelCropDB:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add(self, name, pdf_width, pdf_height, x0, y0, x1, y1, rotation=90):
        with self.db.connect() as conn:
            conn.execute("""
                INSERT INTO label_crops
                (name, pdf_width, pdf_height, crop_x0, crop_y0, crop_x1, crop_y1, rotation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, pdf_width, pdf_height, x0, y0, x1, y1, rotation))