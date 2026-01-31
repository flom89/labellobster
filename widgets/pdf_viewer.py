from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer

from pdf.renderer import render_pdf_page
from .crop_overlay import CropOverlay


class PdfViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setAlignment(Qt.AlignCenter)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(self.graphics_view)

        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        self.pdf_image = None
        self.pdf_rect = None
        self.pixmap_item = None

        # Overlay liegt direkt auf dem PdfViewer, nicht auf dem Viewport
        self.overlay = CropOverlay(aspect_ratio=0, parent=self)
        self.overlay.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Overlay deckt den Bereich des GraphicsView ab
        QTimer.singleShot(0, lambda: self.overlay.setGeometry(self.graphics_view.geometry()))
        QTimer.singleShot(0, self._fit_view)

    def _fit_view(self):
        if self.pixmap_item:
            self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

    def load_pdf(self, path: str):
        # PDF rendern (ohne Rotation!)
        image, pdf_rect, _ = render_pdf_page(path)

        self.pdf_image = image
        self.pdf_rect = pdf_rect
        self.rotated = True   # Wir wissen: Anzeige ist IMMER quer

        # Szene zurücksetzen
        self.scene.clear()
        self.pixmap_item = None

        # PixmapItem erzeugen
        pixmap = QPixmap.fromImage(image)
        self.pixmap_item = self.scene.addPixmap(pixmap)

        # ⭐ WICHTIG: PixmapItem IMMER drehen
        self.pixmap_item.setRotation(90)

        # Ansicht anpassen
        QTimer.singleShot(0, self._fit_view)

        # Overlay korrekt positionieren
        self.overlay.setGeometry(self.graphics_view.geometry())
        self.overlay.raise_()

        print("PDF rendered:", image.width(), "x", image.height())
        print("PDF rect:", self.pdf_rect)
        print("Scene rect:", self.scene.sceneRect())