from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect, QPointF, Signal


class CropOverlay(QWidget):
    cropRectChanged = Signal()
    cropFinalized = Signal()

    def __init__(self, aspect_ratio=None, parent=None, view=None):
        super().__init__(parent)
        self.view = view

        self.aspect_ratio = aspect_ratio
        self.scene_start = None      # Scene-Koordinaten
        self.scene_end = None        # Scene-Koordinaten
        self.is_drawing = False

        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

    # ---------------------------------------------------------
    # Maus-Events (arbeiten NUR in Scene-Koordinaten)
    # ---------------------------------------------------------
    def mousePressEvent(self, event):
        scene_pos = self.view.mapToScene(event.position().toPoint())

        if event.button() == Qt.RightButton:
            self.scene_start = None
            self.scene_end = None
            self.is_drawing = False
            self.update()
            return

        if event.button() == Qt.LeftButton:
            if not self.is_drawing:
                self.scene_start = scene_pos
                self.scene_end = scene_pos
                self.is_drawing = True
            else:
                self.scene_end = self._apply_aspect_ratio_scene(self.scene_start, scene_pos)
                self.is_drawing = False
                self.cropFinalized.emit()

            self.update()

    def mouseMoveEvent(self, event):
        if not self.is_drawing or self.scene_start is None:
            return

        scene_pos = self.view.mapToScene(event.position().toPoint())
        self.scene_end = self._apply_aspect_ratio_scene(self.scene_start, scene_pos)

        self.cropRectChanged.emit()
        self.update()

    # ---------------------------------------------------------
    # Ratio in Scene-Koordinaten
    # ---------------------------------------------------------
    def _apply_aspect_ratio_scene(self, start: QPointF, current: QPointF):
        if not self.aspect_ratio or self.aspect_ratio == 0:
            return current

        dx = current.x() - start.x()
        dy = current.y() - start.y()

        sx = 1 if dx >= 0 else -1
        sy = 1 if dy >= 0 else -1

        adx = abs(dx)
        ady = abs(dy)
        r = self.aspect_ratio

        if adx >= ady:
            width = adx
            height = width / r
        else:
            height = ady
            width = height / r

        return QPointF(start.x() + sx * width, start.y() + sy * height)

    # ---------------------------------------------------------
    # Zeichnen (Scene → Viewport → Overlay)
    # ---------------------------------------------------------
    def paintEvent(self, event):
        if self.scene_start is None or self.scene_end is None:
            return

        # Scene → Viewport
        sp_view = self.view.mapFromScene(self.scene_start)
        ep_view = self.view.mapFromScene(self.scene_end)

        # Viewport → Overlay
        sp = self.mapFromParent(sp_view)
        ep = self.mapFromParent(ep_view)

        rect = QRect(sp, ep).normalized()

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
    # Crop-Rect in Scene-Koordinaten
    # ---------------------------------------------------------
    def get_crop_rect(self):
        if self.scene_start is None or self.scene_end is None:
            return None
        return QRect(self.scene_start.toPoint(), self.scene_end.toPoint()).normalized()

    def set_aspect_ratio(self, ratio):
        self.aspect_ratio = ratio or 0

    def set_crop_rect(self, rect):
        if rect is None:
            self.scene_start = None
            self.scene_end = None
            self.is_drawing = False
            self.update()
            return

        self.scene_start = QPointF(rect.topLeft())
        self.scene_end = QPointF(rect.bottomRight())
        self.is_drawing = False

        self.cropRectChanged.emit()
        self.update()

    # ---------------------------------------------------------
    # Overlay-Geometrie aktualisieren (kein Re-Mapping nötig!)
    # ---------------------------------------------------------
    def update_overlay_geometry(self):
        self.setGeometry(self.view.viewport().rect())
        self.update()