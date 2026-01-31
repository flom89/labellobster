from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect, QPoint


class CropOverlay(QWidget):
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
        # Rechtsklick → Reset
        if event.button() == Qt.RightButton:
            self.start_point = None
            self.current_point = None
            self.final_point = None
            self.is_drawing = False
            self.update()
            return

        # Linksklick → Start oder Endpunkt
        if event.button() == Qt.LeftButton:
            # Startpunkt setzen
            if not self.is_drawing:
                self.start_point = event.pos()
                self.current_point = event.pos()
                self.final_point = None
                self.is_drawing = True
            else:
                # Endpunkt fixieren
                self.final_point = self._apply_aspect_ratio(self.start_point, event.pos())
                self.is_drawing = False

            self.update()

    def mouseMoveEvent(self, event):
        # Live-Zeichnen während der Nutzer die Maus bewegt
        if self.is_drawing and self.start_point:
            self.current_point = self._apply_aspect_ratio(self.start_point, event.pos())
            self.update()

    # ---------------------------------------------------------
    # Seitenverhältnis erzwingen (optional)
    # ---------------------------------------------------------
    def _apply_aspect_ratio(self, start: QPoint, current: QPoint):
        if not self.aspect_ratio:
            return current

        dx = current.x() - start.x()
        dy = current.y() - start.y()

        # Vorzeichen merken
        sx = 1 if dx >= 0 else -1
        sy = 1 if dy >= 0 else -1

        adx = abs(dx)
        ady = abs(dy)

        if adx > ady:
            ady = adx / self.aspect_ratio
        else:
            adx = ady * self.aspect_ratio

        # Vorzeichen wieder anwenden
        dx = sx * adx
        dy = sy * ady

        return QPoint(start.x() + dx, start.y() + dy)



    # ---------------------------------------------------------
    # Zeichnen
    # ---------------------------------------------------------
    def paintEvent(self, event):
        if not self.start_point:
            return

        # Während des Ziehens: current_point, nach Abschluss: final_point
        end = self.final_point if self.final_point else self.current_point
        if not end:
            return

        rect = QRect(self.start_point, end).normalized()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        shade = QColor(0, 0, 0, 200)

        # Oben
        painter.fillRect(0, 0, self.width(), rect.top(), shade)
        # Unten
        painter.fillRect(0, rect.bottom(), self.width(), self.height() - rect.bottom(), shade)
        # Links
        painter.fillRect(0, rect.top(), rect.left(), rect.height(), shade)
        # Rechts
        painter.fillRect(rect.right(), rect.top(), self.width() - rect.right(), rect.height(), shade)

        pen = QPen(QColor(35, 115, 105), 2)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawRect(rect)


    # ---------------------------------------------------------
    # Crop-Rect abrufen
    # ---------------------------------------------------------
    #def get_crop_rect(self):
    #    if not self.start_point:
    #        return None
    #
    #    end = self.final_point if self.final_point else self.current_point
    #    if not end:
    #        return None
    #
    #    return QRect(self.start_point, end).normalized()
    

    def get_crop_rect(self):
        if not self.final_point:
            return None
        return QRect(self.start_point, self.final_point).normalized()

