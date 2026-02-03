from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QGraphicsView, QGraphicsScene, QComboBox, QLabel
)
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtPrintSupport import QPrinter
import win32print
from PySide6.QtGui import QPageSize
from PySide6.QtCore import QSizeF
from PySide6.QtGui import QPageLayout, QPageSize
from PySide6.QtCore import QSizeF
from PySide6.QtCore import Qt




class PrintPreviewDialog(QDialog):
    def __init__(self, image, fmt, dpi, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Druckvorschau")

        self.image = image
        self.fmt = fmt
        self.dpi = dpi

        layout = QVBoxLayout(self)

        # Drucker-Auswahl
        printer_layout = QHBoxLayout()
        printer_layout.addWidget(QLabel("Drucker:"))
        self.cmbPrinters = QComboBox()
        self._load_printers()
        printer_layout.addWidget(self.cmbPrinters)
        layout.addLayout(printer_layout)

        # Vorschau
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        pix = QPixmap.fromImage(image)
        self.scene.addPixmap(pix)
        self.scene.setSceneRect(0, 0, pix.width(), pix.height())

        layout.addWidget(self.view)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_print = QPushButton("Drucken")
        btn_cancel = QPushButton("Abbrechen")

        btn_print.clicked.connect(self._print)
        btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(btn_print)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        # Fenstergröße passend zum Label
        self.setFixedSize(pix.width() + 80, pix.height() + 160)

    def _load_printers(self):

        printers = win32print.EnumPrinters(2)
        for flags, desc, name, comment in printers:
            self.cmbPrinters.addItem(name)

    def _print(self):
        printer_name = self.cmbPrinters.currentText()
        if not printer_name:
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPrinterName(printer_name)

        # Papierformat setzen (Qt6-konform)
        page_size = QPageSize(
            QSizeF(self.fmt.width_mm, self.fmt.height_mm),
            QPageSize.Millimeter
        )
        printer.setPageSize(page_size)

        # Orientierung setzen (Qt6)
        printer.setPageOrientation(QPageLayout.Landscape)

        printer.setFullPage(True)

        painter = QPainter(printer)

        target = painter.viewport()
        size = self.image.size()
        size.scale(target.size(), Qt.KeepAspectRatio)
        painter.setViewport(target.x(), target.y(), size.width(), size.height())
        painter.setWindow(self.image.rect())

        painter.drawImage(0, 0, self.image)
        painter.end()

        self.accept()