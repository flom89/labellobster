from PySide6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout
from forms.ui_mainwindow import Ui_MainWindow
from widgets.pdf_viewer import PdfViewer
from pdf.cropper import widget_rect_to_pdf_rect, crop_pdf
from PySide6.QtCore import QRect, QRectF
from db.database_manager import DatabaseManager
from db.label_format_db import LabelFormatDB
from db.label_crop_db import LabelCropDB


class MainWindow(QMainWindow):
    original_label_path = ''

    def __init__(self):
        super().__init__()

        #Initialize Database
        self.db = DatabaseManager()
        self.format_db = LabelFormatDB(self.db)
        self.crop_db = LabelCropDB(self.db)

        # UI laden
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # PDF Viewer einfügen
        self.pdf_viewer = PdfViewer(self)
        layout = QVBoxLayout(self.ui.pdfContainer)
        layout.addWidget(self.pdf_viewer)

        # Button verbinden
        self.ui.btnOpenFile.clicked.connect(self.open_file)
        self.ui.btnGenerate.clicked.connect(self.genereate_cropped_file)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Datei auswählen",
            "",
            "PDF Dateien (*.pdf);;Alle Dateien (*)"
        )

        if file_path:
            print("Ausgewählte Datei:", file_path)
            self.pdf_viewer.load_pdf(file_path)
            self.original_label_path = file_path

    def genereate_cropped_file(self):
        widget_rect = self.pdf_viewer.overlay.get_crop_rect()
        if widget_rect is None:
            print("Keine Crop-Box gesetzt")
            return

        view = self.pdf_viewer.graphics_view
        pixmap_item = self.pdf_viewer.pixmap_item

        # 1) Overlay → Viewport
        overlay = self.pdf_viewer.overlay
        tl_view = view.mapFromParent(overlay.mapToParent(widget_rect.topLeft()))
        br_view = view.mapFromParent(overlay.mapToParent(widget_rect.bottomRight()))
        rect_view = QRect(tl_view, br_view)

        # 2) Viewport → Scene
        p1_scene = view.mapToScene(rect_view.topLeft())
        p2_scene = view.mapToScene(rect_view.bottomRight())

        # 3) Scene → Pixmap-Koordinaten (Qt macht Rotation automatisch!)
        p1_img = pixmap_item.mapFromScene(p1_scene)
        p2_img = pixmap_item.mapFromScene(p2_scene)

        x0_img = min(p1_img.x(), p2_img.x())
        y0_img = min(p1_img.y(), p2_img.y())
        x1_img = max(p1_img.x(), p2_img.x())
        y1_img = max(p1_img.y(), p2_img.y())

        # 4) Bild → PDF
        img_w = self.pdf_viewer.pdf_image.width()
        img_h = self.pdf_viewer.pdf_image.height()

        pdf_w = self.pdf_viewer.pdf_rect.width
        pdf_h = self.pdf_viewer.pdf_rect.height

        pdf_x0 = x0_img / img_w * pdf_w
        pdf_y0 = y0_img / img_h * pdf_h
        pdf_x1 = x1_img / img_w * pdf_w
        pdf_y1 = y1_img / img_h * pdf_h

        # 5) Sortieren + Clamping
        pdf_x0, pdf_x1 = sorted([pdf_x0, pdf_x1])
        pdf_y0, pdf_y1 = sorted([pdf_y0, pdf_y1])

        pdf_x0 = max(0, min(pdf_x0, pdf_w))
        pdf_x1 = max(0, min(pdf_x1, pdf_w))
        pdf_y0 = max(0, min(pdf_y0, pdf_h))
        pdf_y1 = max(0, min(pdf_y1, pdf_h))

        # 6) PDF croppen
        import fitz
        pdf_rect = fitz.Rect(pdf_x0, pdf_y0, pdf_x1, pdf_y1)

        from pdf.cropper import crop_pdf
        crop_pdf(self.original_label_path, "cropped.pdf", pdf_rect)

        print("Cropped PDF gespeichert.")