from PySide6.QtWidgets import (
    QMainWindow, QFileDialog, QVBoxLayout, QMessageBox, QLabel, QSizePolicy, QWidget
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QPixmap, QPainter, QImage
from PySide6.QtCore import Qt, QTimer, QRect
import fitz
from PySide6.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene

from forms.ui_mainwindow import Ui_MainWindow
from widgets.pdf_viewer import PdfViewer

from db.database_manager import DatabaseManager
from db.paper_formats_db import PaperFormatDB
from db.crop_data_db import CropDataDB
from db.ShippingLabelType_db import ShippingLabelTypeDB

from windows.PaperManager import PaperManager
from windows.SupplierLabelManager import SupplierLabelManager
from modules.PrintPreviewDialog import PrintPreviewDialog
from modules.transformer import Transformer


class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung."""

    original_label_path = ""

    def __init__(self):
        super().__init__()

        # ---------------------------------------------------------
        # Datenbank
        # ---------------------------------------------------------
        self.db = DatabaseManager()
        self.crop_data_db = CropDataDB(self.db)
        self.shipping_label_type_db = ShippingLabelTypeDB(self.db)
        self.paper_format_db = PaperFormatDB(self.db)

        # ---------------------------------------------------------
        # UI laden
        # ---------------------------------------------------------
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lblAutoDetectIndicator.setFixedSize(50, 50)
        self.ui.lblAutoDetectIndicator.setAlignment(Qt.AlignCenter)
        self.ui.lblAutoDetectIndicator.setText("A")
        self.ui.lblAutoDetectIndicator.setStyleSheet("""
            QLabel {
                background-color: #BDBDBD;
                color: #616161;
                font-weight: bold;
                font-size: 24px;
                border-radius: 25px;
                border: 2px solid #9E9E9E;
            }
        """)

        self.current_pdf_path = None

        # ---------------------------------------------------------
        # PDF Viewer (Original)
        # ---------------------------------------------------------
        self.pdf_viewer = PdfViewer(self)
        original_layout = QVBoxLayout(self.ui.pdfContainer)
        original_layout.setContentsMargins(0, 0, 0, 0)
        original_layout.addWidget(self.pdf_viewer)

        # ---------------------------------------------------------
        # Preview (Image)
        # ---------------------------------------------------------
        self.preview_label = QLabel(self.ui.pdfContainer_cropped)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview_label.setMinimumSize(200, 200)  # verhindert Mini-Größe
        self.preview_label.setScaledContents(False)  # bleibt korrekt

        layout = QVBoxLayout(self.ui.pdfContainer_cropped)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.preview_label)

        # ---------------------------------------------------------
        # Comboboxen laden
        # ---------------------------------------------------------
        self._load_format_selector()
        self._load_shipping_label_selector()

        # ---------------------------------------------------------
        # Events verbinden
        # ---------------------------------------------------------
        self.ui.cmbPaperType.currentIndexChanged.connect(self._on_format_changed)
        self.ui.btnManualCrop.clicked.connect(self.generate_cropped_file)
        self.ui.btnPrint.clicked.connect(self.on_print_clicked)
        self.ui.btnSaveCrop.clicked.connect(self.on_save_crop_clicked)

        self.ui.actionImportShippingSlip.triggered.connect(self.open_file)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionShowPaperManager.triggered.connect(self.show_paper_manager)
        self.ui.actionShowSupplierLabelManager.triggered.connect(self.show_supplier_label_manager)
        self.ui.pdfContainer_cropped.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.pdf_viewer.overlay.cropFinalized.connect(self.update_preview)

        # Transformer wird erst gesetzt, wenn ein PDF geladen wurde
        self.transformer = None

    # ---------------------------------------------------------
    # Automatik Indikator befüllen
    # ---------------------------------------------------------
    def _set_indicator(self, success: bool):
        if success:
            self.ui.lblAutoDetectIndicator.setStyleSheet("""
                QLabel {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    font-size: 24px;
                    border-radius: 25px;
                    border: 2px solid #2E7D32;
                }
            """)
        else:
            self.ui.lblAutoDetectIndicator.setStyleSheet("""
                QLabel {
                    background-color: #BDBDBD;
                    color: #616161;
                    font-weight: bold;
                    font-size: 24px;
                    border-radius: 25px;
                    border: 2px solid #9E9E9E;
                }
            """)

    # ---------------------------------------------------------
    # Datei öffnen
    # ---------------------------------------------------------
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Datei auswählen",
            "",
            "PDF Dateien (*.pdf);;Alle Dateien (*)"
        )

        if not file_path:
            return

        self.pdf_viewer.load_pdf(file_path)
        self.current_pdf_path = file_path

    
    def load_crop(self, supplier_label_id, paper_format_id):
        row = self.crop_data_db.get(supplier_label_id, paper_format_id)
        if not row:
            return

        pdf_rect = fitz.Rect(
            row["crop_x0"],
            row["crop_y0"],
            row["crop_x1"],
            row["crop_y1"]
        )

        # PDF → Pixmap
        pixmap_rect = self.transformer.pdf_rect_to_scene_rect(pdf_rect)

        # Pixmap → Scene
        scene_rect = self.transformer.pixmap_item.mapToScene(pixmap_rect).boundingRect()

        # Scene → View
        view_rect = self.pdf_viewer.graphics_view.mapFromScene(scene_rect).boundingRect()

        # View → Overlay
        overlay_rect = self.pdf_viewer.overlay.mapFromParent(view_rect)

        # Overlay setzen
        self.pdf_viewer.overlay.set_crop_rect(overlay_rect)

    # ---------------------------------------------------------
    # Manueller Crop (Preview)
    # ---------------------------------------------------------
    def generate_cropped_file(self):
        if not self.transformer:
            print("Kein PDF geladen.")
            return

        scene_rect = self.pdf_viewer.overlay.get_crop_rect()
        if scene_rect is None:
            print("Keine Crop-Box gesetzt")
            return

        pdf_rect = self.transformer.scene_rect_to_pdf_rect(scene_rect)
        if pdf_rect is None:
            print("Konnte PDF-Rect nicht berechnen.")
            return

        self.update_preview()
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)
    # ---------------------------------------------------------
    # Update Preview
    # ---------------------------------------------------------
    def update_preview(self):
        if not self.transformer:
            return

        rect = self.pdf_viewer.overlay.get_crop_rect()
        if rect is None:
            return

        scene_rect = self.pdf_viewer.overlay.get_crop_rect()
        pdf_rect = self.transformer.scene_rect_to_pdf_rect(scene_rect)

        if pdf_rect is None:
            return

        image = self.transformer.render_cropped_image(pdf_rect, page_index=0)
        if image.isNull():
            return

        pixmap = QPixmap.fromImage(image)

        container_size = self.preview_label.size()

        if container_size.width() < 400 or container_size.height() < 400:
            QTimer.singleShot(50, self.update_preview)
            return


        scaled = pixmap.scaled(
            container_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.preview_label.setPixmap(scaled)

    # ---------------------------------------------------------
    # Papierformate laden
    # ---------------------------------------------------------
    def _load_format_selector(self):
        combo = self.ui.cmbPaperType
        combo.clear()

        combo.addItem("Frei", None)

        for fmt in self.paper_format_db.list_all():
            label = f"{fmt.name} ({fmt.width_mm}×{fmt.height_mm})"
            combo.addItem(label, fmt.id)   # <-- WICHTIG: ID speichern

        # Standardauswahl
        if combo.count() > 1:
            combo.setCurrentIndex(1)
            fmt_id = combo.itemData(1)
            fmt = self.paper_format_db.get_by_id(fmt_id)

            if fmt:
                ratio = max(fmt.width_mm, fmt.height_mm) / min(fmt.width_mm, fmt.height_mm)
                self.current_ratio = ratio
                self.pdf_viewer.overlay.set_aspect_ratio(ratio)
        else:
            self.current_ratio = None

    def _on_format_changed(self, index):
        fmt_id = self.ui.cmbPaperType.itemData(index)

        if fmt_id is None:
            # Frei-Modus
            self.current_ratio = None
            self.pdf_viewer.overlay.set_aspect_ratio(None)
            return

        fmt = self.paper_format_db.get_by_id(fmt_id)
        if not fmt:
            return

        ratio = max(fmt.width_mm, fmt.height_mm) / min(fmt.width_mm, fmt.height_mm)
        self.current_ratio = ratio
        self.pdf_viewer.overlay.set_aspect_ratio(ratio)

    # ---------------------------------------------------------
    # SupplierLabel laden
    # ---------------------------------------------------------
    def _load_shipping_label_selector(self):
        combo = self.ui.cmbShippingLabelType
        combo.clear()

        for row in self.shipping_label_type_db.list_all():
            label = f"{row['carrier']} – {row['label_type']}"
            combo.addItem(label, row["id"])

    # ---------------------------------------------------------
    # Manager öffnen
    # ---------------------------------------------------------
    def show_paper_manager(self):
        dlg = PaperManager(self.paper_format_db, self)
        dlg.exec()
        self._load_format_selector()

    def show_supplier_label_manager(self):
        dlg = SupplierLabelManager(self.shipping_label_type_db, self.paper_format_db, self)
        dlg.exec()
        self._load_shipping_label_selector()

    # ---------------------------------------------------------
    # Crop speichern
    # ---------------------------------------------------------
    def on_save_crop_clicked(self):
        if not self.transformer:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst ein PDF laden.")
            return

        supplier_label_id = self.ui.cmbShippingLabelType.currentData()
        paper_format_id = self.ui.cmbPaperType.currentData()

        if supplier_label_id is None or paper_format_id is None:
            QMessageBox.warning(
                self,
                "Fehler",
                "Bitte Versandlabeltyp und Papierformat auswählen."
            )
            return

        # 1. Lokalen Rect holen (Overlay-Koordinaten)
        local_rect = self.pdf_viewer.overlay.get_crop_rect()
        if local_rect is None:
            QMessageBox.warning(self, "Fehler", "Keine Bounding-Box gesetzt.")
            return

        # ---------------------------------------------------------
        # 2. Overlay → View-Koordinaten (QWidget → QWidget)
        # ---------------------------------------------------------
        tl = self.pdf_viewer.overlay.mapToParent(local_rect.topLeft())
        br = self.pdf_viewer.overlay.mapToParent(local_rect.bottomRight())
        view_rect = QRect(tl, br).normalized()

        # ---------------------------------------------------------
        # 3. View → Scene-Koordinaten (QGraphicsView)
        # ---------------------------------------------------------
        scene_rect = self.pdf_viewer.graphics_view.mapToScene(view_rect).boundingRect()

        # ---------------------------------------------------------
        # 4. Scene → Pixmap-Koordinaten
        # ---------------------------------------------------------
        pixmap_rect = self.transformer.pixmap_item.mapFromScene(scene_rect).boundingRect()

        # ---------------------------------------------------------
        # 5. Pixmap → PDF-Koordinaten
        # ---------------------------------------------------------
        pdf_rect = self.transformer.scene_rect_to_pdf_rect(pixmap_rect)
        if pdf_rect is None:
            QMessageBox.warning(
                self,
                "Fehler",
                "Konnte PDF-Bounding-Box nicht berechnen."
            )
            return

        x0, y0, x1, y1 = pdf_rect.x0, pdf_rect.y0, pdf_rect.x1, pdf_rect.y1

        existing = self.crop_data_db.get(supplier_label_id, paper_format_id)
        if existing:
            reply = QMessageBox.question(
                self,
                "Crop überschreiben?",
                "Für diesen Labeltyp und dieses Papierformat existiert bereits ein Crop.\n"
                "Möchtest du ihn überschreiben?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        # 6. Speichern
        self.crop_data_db.add_or_update(
            supplier_label_id,
            paper_format_id,
            x0, y0, x1, y1,
            rotation=0
        )

        QMessageBox.information(
            self,
            "Gespeichert",
            "Die Bounding-Box wurde erfolgreich gespeichert."
        )

        self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)

    # ---------------------------------------------------------
    # Schauen ob Match vorhanden
    # ---------------------------------------------------------
    def _auto_detect_crop(self):
        if not self.transformer:
            self._set_indicator(False)
            return

        supplier_label_id = self.ui.cmbShippingLabelType.currentData()
        paper_format_id = self.ui.cmbPaperType.currentData()

        keywords = self.shipping_label_type_db.get_keywords(supplier_label_id)
        if not keywords:
            self._set_indicator(False)
            return

        text = ""
        for page_index in range(self.transformer.pdf_document.page_count):
            page = self.transformer.pdf_document.load_page(page_index)
            text += page.get_text("text").lower()

        all_match = all(kw.lower() in text for kw in keywords)

        if not all_match:
            self._set_indicator(False)
            return

        self._set_indicator(True)

        crop = self.crop_data_db.get(supplier_label_id, paper_format_id)
        if not crop:
            return

        pdf_rect = self.crop_data_db.get_rect(supplier_label_id, paper_format_id)

        widget_rect = self.transformer.pdf_rect_to_overlay_rect(
            self.pdf_viewer.overlay,
            pdf_rect
        )

        self.pdf_viewer.overlay.set_crop_rect(widget_rect)
        self.update_preview()
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)

    # ---------------------------------------------------------
    # Wird vom PdfViewer nach stabilem fitInView aufgerufen
    # ---------------------------------------------------------
    def on_pdf_ready(self):
        self.transformer = Transformer(
            view=self.pdf_viewer.graphics_view,
            pixmap_item=self.pdf_viewer.pixmap_item,
            pdf_image=self.pdf_viewer.pdf_image,
            pdf_rect=self.pdf_viewer.pdf_rect,
            pdf_document=self.pdf_viewer.pdf_document,
            original_pdf_path=self.current_pdf_path
        )

        self.pdf_viewer.overlay.setEnabled(True)

        # Auto-Detect zuerst
        QTimer.singleShot(0, self._auto_detect_crop)

    # ---------------------------------------------------------
    # Drucken
    # ---------------------------------------------------------
    def on_print_clicked(self):
        # Scene-Rect holen
        scene_rect = self.pdf_viewer.overlay.get_crop_rect()
        if scene_rect is None:
            QMessageBox.warning(self, "Fehler", "Keine Bounding-Box gesetzt.")
            return

        # Scene → PDF
        pdf_rect = self.transformer.scene_rect_to_pdf_rect(scene_rect)
        if pdf_rect is None:
            QMessageBox.warning(self, "Fehler", "Konnte PDF-Bounding-Box nicht berechnen.")
            return

        # Papierformat aus DB holen
        fmt_id = self.ui.cmbPaperType.currentData()
        fmt = self.paper_format_db.get_by_id(fmt_id)

        if fmt is None:
            QMessageBox.warning(self, "Fehler", "Ungültiges Papierformat ausgewählt.")
            return

        dpi = 300
        width_px  = int(fmt.width_mm  / 25.4 * dpi)
        height_px = int(fmt.height_mm / 25.4 * dpi)

        preview_img = self.transformer.render_cropped_image(pdf_rect, dpi=dpi)
        preview_img = preview_img.scaled(width_px, height_px, Qt.KeepAspectRatio)

        dlg = PrintPreviewDialog(preview_img, fmt, dpi, self)
        dlg.exec()

