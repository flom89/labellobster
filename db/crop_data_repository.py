# repository_crop_data.py
from sqlalchemy.orm import Session
from db.models import CropData

class CropDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, supplier_label_id: int, paper_format_name: str, printer_name: str):
        # 1. Bruteforce-Check: Was existiert ÜBERHAUPT in dieser Tabelle?
        total_count = self.session.query(CropData).count()
        print(f"DEBUG_DATABASE: Gesamtzahl Einträge in CropData: {total_count}")

        all_rows = self.session.query(CropData).all()
        for r in all_rows:
            print(
                f"DEBUG_DATABASE: Vorhanden -> ID:{r.supplier_label_id} (Typ:{type(r.supplier_label_id)}) | Printer:{r.printer_name}")

        # ... (restliche get-Logik)
        # 1. Typ-Sicherheit erzwingen
        try:
            s_id = int(supplier_label_id)
        except:
            s_id = supplier_label_id

        # 2. Alle Einträge für diese ID holen (Breitband-Suche)
        all_potential = self.session.query(CropData).filter_by(supplier_label_id=s_id).all()

        print(f"--- REPO DEBUG START ---")
        print(f"Gesucht: ID={s_id} | Paper='{paper_format_name}' | Printer='{printer_name}'")
        print(f"Einträge in DB für ID {s_id}: {len(all_potential)}")

        for row in all_potential:
            # Vergleich mit sichtbaren Markierungen (|), um Leerzeichen zu finden
            p_match = (row.paper_format_name == paper_format_name)
            pr_match = (row.printer_name == printer_name)

            print(f"Check DB-Zeile: Paper='|{row.paper_format_name}|' (Match: {p_match})")
            print(f"Check DB-Zeile: Printer='|{row.printer_name}|' (Match: {pr_match})")

            if p_match and pr_match:
                print(">>> MATCH GEFUNDEN!")
                return row

        print("--- REPO DEBUG ENDE (KEIN MATCH) ---")
        return None

    def get_by_label(self, supplier_label_id: int):
        return (
            self.session.query(CropData)
            .filter_by(supplier_label_id=supplier_label_id)
            .first()
        )

    def get_all_by_label_id(self, label_id: int):
        """
        Gibt alle gespeicherten Boundingbox-Konfigurationen für einen Label-Typ zurück.
        """
        from db.models import CropData # Falls nicht schon oben importiert
        return (
            self.session.query(CropData)
            .filter_by(supplier_label_id=label_id)
            .all()
        )

    def add_or_update(self, label_id, printer, paper, x0, y0, x1, y1, rotation):
        # Wir suchen nach der EXAKTEN Kombination aus dem "Dreiklang"
        existing = self.session.query(CropData).filter_by(
            supplier_label_id=label_id,
            printer_name=printer,
            paper_format_name=paper
        ).first()

        if existing:
            # Nur wenn Label + Drucker + Papier gleich sind, wird aktualisiert
            print(f"DEBUG_REPO: Update bestehender Box (ID:{label_id}, Printer:{printer}, Paper:{paper})")
            existing.crop_x0, existing.crop_y0 = x0, y0
            existing.crop_x1, existing.crop_y1 = x1, y1
            existing.rotation = rotation
        else:
            # Wenn eine der drei Komponenten abweicht -> Neuer Datensatz!
            print(f"DEBUG_REPO: Erstelle NEUEN Datensatz (ID:{label_id}, Printer:{printer}, Paper:{paper})")
            new_crop = CropData(
                supplier_label_id=label_id,
                printer_name=printer,
                paper_format_name=paper,
                crop_x0=x0, crop_y0=y0,
                crop_x1=x1, crop_y1=y1,
                rotation=rotation
            )
            self.session.add(new_crop)

        self.session.commit()