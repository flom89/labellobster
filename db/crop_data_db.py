import fitz

class CropDataDB:
    def __init__(self, db):
        self.db = db

    def add_or_update(self, supplier_label_id, paper_format_id,
                      x0, y0, x1, y1, rotation=0):
        with self.db.connect() as conn:
            conn.execute("""
                INSERT INTO crop_data
                (supplier_label_id, paper_format_id,
                 crop_x0, crop_y0, crop_x1, crop_y1, rotation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(supplier_label_id, paper_format_id)
                DO UPDATE SET
                    crop_x0 = excluded.crop_x0,
                    crop_y0 = excluded.crop_y0,
                    crop_x1 = excluded.crop_x1,
                    crop_y1 = excluded.crop_y1,
                    rotation = excluded.rotation
            """, (supplier_label_id, paper_format_id,
                  x0, y0, x1, y1, rotation))

    def get(self, supplier_label_id, paper_format_id):
        with self.db.connect() as conn:
            cur = conn.execute("""
                SELECT *
                FROM crop_data
                WHERE supplier_label_id = ? AND paper_format_id = ?
            """, (supplier_label_id, paper_format_id))
            return cur.fetchone()

    def delete(self, supplier_label_id, paper_format_id):
        with self.db.connect() as conn:
            conn.execute("""
                DELETE FROM crop_data
                WHERE supplier_label_id = ? AND paper_format_id = ?
            """, (supplier_label_id, paper_format_id))

    def get_rect(self, supplier_label_id, paper_format_id):
        row = self.get(supplier_label_id, paper_format_id)
        if not row:
            print("NO CROP FOUND")
            return None

        print("CROP ROW:", dict(row))

        return fitz.Rect(
            row["crop_x0"],
            row["crop_y0"],
            row["crop_x1"],
            row["crop_y1"]
        )
