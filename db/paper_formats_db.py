class PaperFormatDB:
    def __init__(self, db):
        self.db = db

    def add(self, name, width_mm, height_mm):
        with self.db.connect() as conn:
            conn.execute("""
                INSERT INTO paper_formats (name, width_mm, height_mm)
                VALUES (?, ?, ?)
            """, (name, width_mm, height_mm))

    def update(self, id, name, width_mm, height_mm):
        with self.db.connect() as conn:
            conn.execute("""
                UPDATE paper_formats
                SET name = ?, width_mm = ?, height_mm = ?
                WHERE id = ?
            """, (name, width_mm, height_mm, id))

    def delete(self, id):
        with self.db.connect() as conn:
            conn.execute("DELETE FROM paper_formats WHERE id = ?", (id,))

    def list_all(self):
        with self.db.connect() as conn:
            rows = conn.execute("""
                SELECT id, name, width_mm, height_mm
                FROM paper_formats
                ORDER BY name ASC
            """).fetchall()

        from db.models import PaperFormat
        return [PaperFormat(*row) for row in rows]

    def get_by_id(self, id):
        with self.db.connect() as conn:
            row = conn.execute("""
                SELECT id, name, width_mm, height_mm
                FROM paper_formats
                WHERE id = ?
            """, (id,)).fetchone()

        from db.models import PaperFormat
        return PaperFormat(*row) if row else None

    def get_by_name(self, name):
        with self.db.connect() as conn:
            row = conn.execute("""
                SELECT id, name, width_mm, height_mm
                FROM paper_formats
                WHERE name = ?
            """, (name,)).fetchone()

        from db.models import PaperFormat
        return PaperFormat(*row) if row else None