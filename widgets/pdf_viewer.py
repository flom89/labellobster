from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import fitz

from widgets.crop_overlay import CropOverlay
from pdf.renderer import render_pdf_page


class PdfViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pdf_loaded = False

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # View
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setAlignment(Qt.AlignCenter)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.graphics_view)

        # Scene
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        # PDF internals
        self.pdf_image = None
        self.pdf_rect = None
        self.pdf_page = None
        self.pixmap_item = None
        self.pdf_document = None

        # Overlay (Kind des Viewports)
        self.overlay = CropOverlay(aspect_ratio=0, parent=self.graphics_view.viewport())
        self.overlay.setGeometry(self.graphics_view.viewport().rect())
        self.overlay.raise_()
        self.overlay.setEnabled(False)

    # ---------------------------------------------------------
    # Resize: PDF und Overlay neu synchronisieren
    # ---------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # FitInView NICHT direkt aufrufen → Endlosschleife
        QTimer.singleShot(0, self._refit_after_resize)

    def _refit_after_resize(self):
        if not self.pixmap_item:
            return

        # PDF neu einpassen
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

        # Overlay an neuen Viewport anpassen
        if self.graphics_view.viewport() is not None:
            self.overlay.setGeometry(self.graphics_view.viewport().rect())
            self.overlay.raise_()

    # ---------------------------------------------------------
    # Fit view (nur beim Laden)
    # ---------------------------------------------------------
    def _fit_view_initial(self):
        if not self.pixmap_item:
            return

        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

        if self.graphics_view.viewport() is not None:
            self.overlay.setGeometry(self.graphics_view.viewport().rect())
            self.overlay.raise_()
            self.overlay.setEnabled(True)

        # MainWindow informieren
        win = self.window()
        if hasattr(win, "on_pdf_ready"):
            win.on_pdf_ready()

    # ---------------------------------------------------------
    # PDF laden
    # ---------------------------------------------------------
    def load_pdf(self, path: str):
        self.pdf_loaded = False
        self.overlay.setEnabled(False)

        # PDF öffnen
        self.pdf_document = fitz.open(path)

        # Seite rendern
        image, pdf_page, pdf_rect, _ = render_pdf_page(path)
        self.pdf_image = image
        self.pdf_page = pdf_page
        self.pdf_rect = pdf_rect

        # Szene zurücksetzen
        self.scene.clear()

        # PixmapItem erzeugen
        pixmap = QPixmap.fromImage(image)
        self.pixmap_item = self.scene.addPixmap(pixmap)

        # SceneRect korrekt setzen
        bounds = self.pixmap_item.mapToScene(self.pixmap_item.boundingRect()).boundingRect()
        self.scene.setSceneRect(bounds)

        self.pdf_loaded = True

        # Overlay initial setzen
        if self.graphics_view.viewport() is not None:
            self.overlay.setGeometry(self.graphics_view.viewport().rect())
            self.overlay.raise_()

        # FitInView erst nach Layout-Stabilisierung
        QTimer.singleShot(0, self._fit_view_initial)