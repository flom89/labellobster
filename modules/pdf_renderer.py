import fitz  # PyMuPDF
from PySide6.QtGui import QImage, QPixmap


class PDFRenderer:
    def __init__(self, filename):
        self.doc = fitz.open(filename)

    def get_page_pixmap(self, page_number=0, dpi=150):
        """Konvertiert eine PDF-Seite in ein QPixmap."""
        page = self.doc.load_page(page_number)

        # Zoom berechnen (72 DPI ist Standard im PDF)
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=matrix)

        # Bild-Format bestimmen
        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888

        # QImage aus den Rohdaten des Pixmaps erstellen
        qt_image = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            fmt
        )

        return QPixmap.fromImage(qt_image), page.rect

    def get_page_text(self, page_index: int) -> str:
        """Extrahiert den Rohtext einer bestimmten Seite."""
        try:
            # Falls du fitz (PyMuPDF) nutzt:
            page = self.doc.load_page(page_index)
            return page.get_text()
        except Exception as e:
            print(f"Renderer-Fehler bei Textextraktion: {e}")
            return ""