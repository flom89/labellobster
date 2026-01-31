import sqlite3
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LabelFormat:
    id: int
    name: str
    width_mm: float
    height_mm: float

    @property
    def aspect_ratio(self) -> float:
        """Height / Width – e.g. 199/103 for DHL 103x199."""
        return self.height_mm / self.width_mm
    
class LabelCropDB:
    def __init__(self, db_path: str = "label_formats.db"):
        self.db_path = db_path
        self._init_db()



class LabelFormatDB:
    def __init__(self, db_path: str = "label_formats.db"):
        """
        db_path: Path to the SQLite file, e.g. 'label_formats.db'
        """
        self.db_path = db_path
        self._init_db()

    # ---------------------------------------------------------
    # internal helpers
    # ---------------------------------------------------------
    def _init_db(self) -> None:
        with self._connect() as conn:
            # ---------------------------------------------------------
            # 1) label_formats (physische Etikettenformate)
            # ---------------------------------------------------------
            conn.execute("""
                CREATE TABLE IF NOT EXISTS label_formats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    width_mm REAL NOT NULL,
                    height_mm REAL NOT NULL
                );
            """)

            # ---------------------------------------------------------
            # 2) label_crops (gespeicherte PDF-Crop-Definitionen)
            # ---------------------------------------------------------
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

            # ---------------------------------------------------------
            # 3) Migration: fehlende Spalten automatisch hinzufügen
            # ---------------------------------------------------------
            def ensure_columns(table, required_cols):
                existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
                for col, sql in required_cols.items():
                    if col not in existing:
                        conn.execute(sql)

            # Migration für label_formats (falls du später erweiterst)
            ensure_columns("label_formats", {
                # Beispiel für zukünftige Erweiterungen:
                # "dpi": "ALTER TABLE label_formats ADD COLUMN dpi INTEGER DEFAULT 300;"
            })

            # Migration für label_crops
            ensure_columns("label_crops", {
                "rotation": "ALTER TABLE label_crops ADD COLUMN rotation INTEGER DEFAULT 90;",
                "created_at": "ALTER TABLE label_crops ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP;"
            })


    # ---------------------------------------------------------
    # CRUD operations
    # ---------------------------------------------------------
    def add(self, name: str, width_mm: float, height_mm: float) -> None:
        """
        Adds a new label format.
        Example:
            db.add("DHL 103x199", 103, 199)
        """
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO label_formats (name, width_mm, height_mm) VALUES (?, ?, ?)",
                (name, width_mm, height_mm)
            )

    def delete(self, id: int) -> None:
        """Deletes a label format by ID."""
        with self._connect() as conn:
            conn.execute("DELETE FROM label_formats WHERE id = ?", (id,))

    def update(self, id: int, name: str, width_mm: float, height_mm: float) -> None:
        """Updates an existing label format."""
        with self._connect() as conn:
            conn.execute(
                "UPDATE label_formats SET name = ?, width_mm = ?, height_mm = ? WHERE id = ?",
                (name, width_mm, height_mm, id)
            )

    def list_all(self) -> List[LabelFormat]:
        """Returns all label formats as LabelFormat objects."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, width_mm, height_mm FROM label_formats ORDER BY name ASC"
            ).fetchall()
            return [LabelFormat(*row) for row in rows]

    def get_by_id(self, id: int) -> Optional[LabelFormat]:
        """Fetches a single label format by ID."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, name, width_mm, height_mm FROM label_formats WHERE id = ?",
                (id,)
            ).fetchone()
            return LabelFormat(*row) if row else None

    def get_by_name(self, name: str) -> Optional[LabelFormat]:
        """Fetches a label format by exact name."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, name, width_mm, height_mm FROM label_formats WHERE name = ?",
                (name,)
            ).fetchone()
            return LabelFormat(*row) if row else None