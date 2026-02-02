class ShippingLabelTypeDB:
    def __init__(self, db):
        self.db = db

    def add(self, carrier, label_type, keywords, format_id):
        self.db.execute(
            """
            INSERT INTO ShippingLabelType_definitions
            (carrier, label_type, keywords, format_id)
            VALUES (?, ?, ?, ?)
            """,
            (carrier, label_type, keywords, format_id)
        )

    def update(self, id, carrier, label_type, keywords, format_id):
        self.db.execute(
            """
            UPDATE ShippingLabelType_definitions
            SET carrier = ?, label_type = ?, keywords = ?, format_id = ?
            WHERE id = ?
            """,
            (carrier, label_type, keywords, format_id, id)
        )

    def delete(self, id):
        self.db.execute(
            "DELETE FROM ShippingLabelType_definitions WHERE id = ?",
            (id,)
        )

    def list_all(self):
        cursor = self.db.execute(
            """
            SELECT *
            FROM ShippingLabelType_definitions
            ORDER BY carrier, label_type
            """
        )
        return cursor.fetchall()

    def get_by_id(self, id):
        cursor = self.db.execute(
            """
            SELECT *
            FROM ShippingLabelType_definitions
            WHERE id = ?
            """,
            (id,)
        )
        rows = cursor.fetchall()
        return rows[0] if rows else None
    
    def get_keywords(self, id):
        row = self.get_by_id(id)
        if not row:
            return []

        raw = row["keywords"]
        if not raw:
            return []

        # CSV → Liste
        return [kw.strip() for kw in raw.split(",") if kw.strip()]