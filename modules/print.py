import os
import time

from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QPainter, QImage, Qt, QColor, QTransform
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPrintSupport import QPrinterInfo, QPrinter
from sqlalchemy import String


def wait_and_delete_file(filepath, timeout=30, interval=1):
    """
    Wartet, bis eine Datei nicht mehr blockiert ist, und löscht sie dann.
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        if not os.path.exists(filepath):
            return True  # Datei existiert bereits nicht mehr

        try:
            os.remove(filepath)
            print(f"Datei {filepath} erfolgreich gelöscht.")
            return True
        except OSError:
            # Datei ist wahrscheinlich noch in Benutzung (besonders unter Windows)
            time.sleep(interval)

    print(f"Timeout: Datei {filepath} konnte nicht gelöscht werden.")
    return False


class PrintingSystem:
    def __init__(self):
        self.printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        self.available_printers = QPrinterInfo.availablePrinters()
        return

    def set_printer(self, printer):
        self.printer.setPrinterName(printer)

    def get_available_printers(self):
        return self.available_printers

    def load_paper_formats(self):
        info = QPrinterInfo(self.printer)
        paper_formats =  info.supportedPageSizes()
        return paper_formats

    def get_selected_paper_information(self):
        actual_page_size  = self.printer.pageLayout().pageSize()
        return actual_page_size

    def print_pdf(self, pdf_path: str) -> bool:
        if not os.path.exists(pdf_path): return False

        doc = QPdfDocument()
        doc.load(pdf_path)
        if doc.status() != QPdfDocument.Status.Ready: return False

        # 1. Drucker-Geometrie abfragen (203 DPI)
        dpi = self.printer.resolution()
        layout = self.printer.pageLayout()
        paint_rect = layout.paintRectPixels(dpi)  # Der vom Treiber erlaubte Bereich

        painter = QPainter()
        if not painter.begin(self.printer): return False

        for i in range(doc.pageCount()):
            if i > 0: self.printer.newPage()

            # 2. PDF-Größe in Pixeln berechnen (ohne Skalierungs-Verzerrung)
            pdf_size_pt = doc.pagePointSize(i)
            scale = dpi / 72.0
            nw = int(pdf_size_pt.width() * scale)
            nh = int(pdf_size_pt.height() * scale)

            # 3. Rendern in nativer Auflösung
            raw_img = doc.render(i, QSize(nw, nh))

            # 4. Hintergrund füllen (Verhindert Schwarz-Druck bei Transparenz)
            final_img = QImage(QSize(nw, nh), QImage.Format.Format_RGB32)
            final_img.fill(QColor("white"))
            tmp_painter = QPainter(final_img)
            tmp_painter.drawImage(0, 0, raw_img)
            tmp_painter.end()

            # 5. Rotation (Falls das PDF quer zum Papier liegt)
            pdf_is_land = nw > nh
            paper_is_land = paint_rect.width() > paint_rect.height()
            if pdf_is_land != paper_is_land:
                final_img = final_img.transformed(QTransform().rotate(90))

            # 6. Einpassen in den Druckbereich
            # Wir skalieren das Bild nur, wenn es über den Paint-Bereich hinausragt
            if final_img.width() > paint_rect.width() or final_img.height() > paint_rect.height():
                final_img = final_img.scaled(
                    paint_rect.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

            # 7. Positionierung unter Berücksichtigung der Seitenränder (Margins)
            # p_rect.left/top sind die vom Treiber gemeldeten Offsets (12px/24px)
            x_final = paint_rect.left() + (paint_rect.width() - final_img.width()) // 2
            y_final = paint_rect.top() + (paint_rect.height() - final_img.height()) // 2

            # 1:1 Ausgabe an der berechneten Position
            painter.drawImage(QPoint(x_final, y_final), final_img)

        painter.end()
        doc.close()

        del painter
        del doc


        wait_and_delete_file(pdf_path)
        return True

    def get_current_paper_ratio(self) -> float:
        layout = self.printer.pageLayout()
        # paintRectPixels berücksichtigt die aktuelle Orientierung des Druckers!
        rect = layout.paintRectPixels(self.printer.resolution())

        if rect.height() > 0:
            # Hier kommt jetzt automatisch 0.66 (Hoch) oder 1.5 (Quer) raus,
            # je nachdem was im Druckerdialog/System eingestellt ist.
            return rect.width() / rect.height()
        return 1.0