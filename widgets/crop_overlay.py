from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect, QPoint, Signal


class CropOverlay(QWidget):
    cropRectChanged = Signal()
    cropFinalized = Signal()

    def __init__(self, aspect_ratio=None, parent=None):
        super().__init__(parent)

        self.aspect_ratio = aspect_ratio
        self.start_point = None
        self.current_point = None
        self.final_point = None
        self.is_drawing = False

        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

    # ---------------------------------------------------------
    # Maus-Events
    # ---------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.start_point = None
            self.current_point = None
            self.final_point = None
            self.is_drawing = False
            self.update()
            return

        if event.button() == Qt.LeftButton:
            if not self.is_drawing:
                self.start_point = event.pos()
                self.current_point = event.pos()
                self.final_point = None
                self.is_drawing = True
            else:
                self.final_point = self._apply_aspect_ratio(self.start_point, event.pos())
                self.is_drawing = False
                self.cropFinalized.emit()

            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing and self.start_point:
            self.current_point = self._apply_aspect_ratio(self.start_point, event.pos())
            self.cropRectChanged.emit()
            self.update()

    # ---------------------------------------------------------
    # Photoshop-Style Ratio Enforcement
    # ---------------------------------------------------------
    def _apply_aspect_ratio(self, start: QPoint, current: QPoint):
        if not self.aspect_ratio or self.aspect_ratio == 0:
            return current

        raw_dx = current.x() - start.x()
        raw_dy = current.y() - start.y()


        sx = 1 if raw_dx >= 0 else -1
        sy = 1 if raw_dy >= 0 else -1

        adx = abs(raw_dx)
        ady = abs(raw_dy)
        r = self.aspect_ratio  # jetzt immer >= 1

        # Orientierung NUR aus der Mausbewegung
        if adx >= ady:
            # Querformat
            width = adx
            height = width / r
        else:
            # Hochformat
            height = ady
            width = height / r

        dx = sx * width
        dy = sy * height

        return QPoint(start.x() + dx, start.y() + dy)

    # ---------------------------------------------------------
    # Zeichnen
    # ---------------------------------------------------------
    def paintEvent(self, event):
        if not self.start_point:
            return

        end = self.final_point if self.final_point else self.current_point
        if not end:
            return

        rect = QRect(self.start_point, end).normalized()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        shade = QColor(0, 0, 0, 200)

        painter.fillRect(0, 0, self.width(), rect.top(), shade)
        painter.fillRect(0, rect.bottom(), self.width(), self.height() - rect.bottom(), shade)
        painter.fillRect(0, rect.top(), rect.left(), rect.height(), shade)
        painter.fillRect(rect.right(), rect.top(), self.width() - rect.right(), rect.height(), shade)

        pen = QPen(QColor(35, 115, 105), 2)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawRect(rect)

    # ---------------------------------------------------------
    # Crop-Rect abrufen
    # ---------------------------------------------------------
    def get_crop_rect(self):
        if not self.final_point:
            return None
        return QRect(self.start_point, self.final_point).normalized()

    def set_aspect_ratio(self, ratio):
        if ratio is None:
            ratio = 0
        self.aspect_ratio = ratio

    def set_crop_rect(self, rect: QRect):
        """
        Setzt die Crop-Boundingbox von außen (z.B. Auto-Detect).
        """
        if rect is None:
            self.start_point = None
            self.current_point = None
            self.final_point = None
            self.is_drawing = False
            self.update()
            return

        self.start_point = rect.topLeft()
        self.current_point = rect.bottomRight()
        self.final_point = rect.bottomRight()
        self.is_drawing = False

        self.cropRectChanged.emit()
        self.update()