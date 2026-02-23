from typing import cast, Any

from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPen
from PySide6.QtGui import QPainterPath, QBrush, QColor
from PySide6.QtWidgets import QGraphicsItem


class ResizeHandle(QGraphicsRectItem):
    def __init__(self, parent: QGraphicsItem):
        super().__init__(QRectF(-5, -5, 10, 10), parent)
        self.ratio = None
        self.base_ratio = None
        self.setBrush(QColor("black"))
        self.setPen(QPen(QColor("red"), 25))

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setCursor(Qt.CursorShape.SizeFDiagCursor)

        # Z-Value innerhalb des Parents erhöhen, damit er ÜBER der Box-Linie liegt
        self.setZValue(1.0)

        # WICHTIG: Der Handle muss Klicks abfangen, bevor das Parent sie sieht
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Wir holen das Parent-Objekt
            p: Any = self.parentItem()

            # Wir prüfen dynamisch, ob das Parent-Objekt unsere Box ist
            if p and hasattr(p, "update_from_handle"):
                # Jetzt rufen wir die Methode auf dem Parent auf, nicht auf self!
                if not p.is_updating:
                    p.update_from_handle(value)

        return super().itemChange(change, value)

    def mouseMoveEvent(self, event):
        # Wir holen das Parent-Item
        box = self.parentItem()

        # DEBUG-PRINT: Wer ist mein Parent wirklich?
        print(f"DEBUG: Ich bin ein Handle. Mein Parent ist: {box}")

        if box:
            # Wir berechnen die Position relativ zur Box
            pos_in_box = self.mapToParent(event.pos())

            # WICHTIG: Wir rufen die Methode auf.
            # Wenn die IDE hier meckert, ignorieren wir das jetzt für den Test!
            try:
                box.update_from_handle(pos_in_box)
                print("DEBUG: Box-Methode erfolgreich aufgerufen!")
            except Exception as e:
                print(f"DEBUG: Fehler beim Aufruf der Box: {e}")

        super().mouseMoveEvent(event)

    def update_position(self):
        # Setzt den Handle immer an die untere rechte Ecke des Rects
        r = self.parentItem().rect()
        self.setPos(r.right(), r.bottom())


class AspectBox(QGraphicsRectItem):
    def __init__(self, x: float, y: float, ratio: float):
        # Falls ratio None ist, nutze 1.5 als Sicherheitsnetz
        safe_ratio = ratio if (ratio and ratio > 0) else 1.5
        # Initialisierung wie gehabt
        super().__init__(0, 0, 100, 100 / ratio)
        self.base_ratio = safe_ratio
        self._is_updating = False
        self.ratio = ratio

        self.setPen(QPen(QColor("red"), 7, Qt.PenStyle.DotLine))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.handle = ResizeHandle(self)
        self.setPos(x, y)
        self.update_handle_visuals()

    def contextMenuEvent(self, event):
        self.reset_aspect_box()
        event.accept()

    def reset_aspect_box(self):
        # 1. Die View finden, die dieses Item gerade anzeigt
        views = self.scene().views() if self.scene() else []
        if not views:
            return

        view = views[0]  # Wir nehmen die erste aktive View

        # 2. Logik-Reset: Wir setzen die Box auf ein Quadrat (Ratio 1.0)
        # Wenn du das ursprüngliche Ratio behalten willst: self.ratio = self.base_ratio
        self.ratio = 1.0
        new_w, new_h = 50.0, 50.0
        self.setRect(0, 0, new_w, new_h)

        # 3. In der Mitte der View zentrieren
        # HIER nutzen wir die View, um das Zentrum zu berechnen
        view_rect = view.viewport().rect()
        scene_center = view.mapToScene(view_rect.center())

        # Position setzen (Zentrum minus halbe Breite/Höhe)
        self.setPos(scene_center.x() - (new_w / 2),
                    scene_center.y() - (new_h / 2))

        # 4. Bestehende Update-Logik nutzen
        self.update_handle_visuals()
        self.update()

    def update_from_handle(self, handle_pos: QPointF):
        # Wichtig: Falls du die Sperre wieder einbaust, nutze try/finally
        self._is_updating = True
        try:
            # 1. Aktuelle Mausposition
            mx = max(20.0, handle_pos.x())
            my = max(20.0, handle_pos.y())

            # 2. FLIP-LOGIK:
            # Wenn Maus-X > Maus-Y -> Wir wollen Landscape (r > 1.0)
            # Wenn Maus-Y > Maus-X -> Wir wollen Portrait (r < 1.0)
            mouse_wants_landscape = mx > my
            current_is_landscape = self.ratio > 1.0

            if mouse_wants_landscape != current_is_landscape:
                self.prepareGeometryChange()
                # Der magische 90-Grad-Flip
                self.ratio = 1.0 / self.ratio
                print(f">>> FLIP! Neues Ratio: {self.ratio:.2f}")

            # 3. GEOMETRIE BERECHNEN
            # Wir nehmen die längere Seite der Mausbewegung als Basis für die Breite
            # oder bleiben bei MX - Hauptsache das Ratio wird angewendet:
            new_w = mx
            new_h = new_w / self.ratio

            # 4. ANWENDUNG
            self.prepareGeometryChange()
            self.setRect(0, 0, new_w, new_h)

            # 5. HANDLE POSITIONIEREN - Der "Sticky-Fix"
            if hasattr(self, 'handle') and self.handle:
                # Wir nehmen NICHT die Mausposition mx/my,
                # sondern die ECHTEN berechneten Maße der Box:
                current_rect = self.rect()
                self.handle.setPos(current_rect.width(), current_rect.height())

            self.update()
            print(f"BOX-UPDATE: w={new_w:.1f}, h={new_h:.1f}, r={self.ratio:.2f}")

        finally:
            self._is_updating = False

    def set_ratio(self, new_ratio: float):
        if not new_ratio or new_ratio <= 0: return
        self.prepareGeometryChange()
        self.ratio = new_ratio

        # Bestehende Breite halten, Höhe anpassen
        w = self.rect().width()
        self.setRect(0, 0, w, w / self.ratio)

        # HANDLE POSITION ZWINGEN
        if hasattr(self, 'handle') and self.handle:
            self.handle.setPos(w, w / self.ratio)
        self.update()

    def flip_ratio(self):
        """Tauscht Breite und Höhe (90 Grad Flip)"""
        self.prepareGeometryChange()
        self.ratio = 1.0 / self.ratio
        self._update_rect_by_ratio()

    def _update_rect_by_ratio(self):
        curr_w = self.rect().width()
        self.setRect(0, 0, curr_w, curr_w / self.ratio)
        if hasattr(self, 'update_handle_visuals'):
            self.update_handle_visuals()


    @property
    def is_updating(self) -> bool:
        return self._is_updating

    def update_handle_visuals(self):
        """Setzt den Handle auf die Ecke. WICHTIG: Nutze Koordinaten, nicht das Objekt selbst."""
        self._is_updating = True
        r = self.rect()
        # Korrekt: x und y Werte übergeben
        self.handle.setPos(r.right(), r.bottom())
        self._is_updating = False

    def set_size_by_width(self, width_px: float):
        h = width_px / self.ratio
        self.setRect(0, 0, width_px, h)
        self.update_handle_visuals()

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange and self.scene():
            #s_rect = self.scene().sceneRect()
            #i_rect = self.rect()
            #nx = max(s_rect.left(), min(value.x(), s_rect.right() - i_rect.width()))
            #ny = max(s_rect.top(), min(value.y(), s_rect.bottom() - i_rect.height()))

            if self.scene():
                self.scene().update()  # Erzwingt Neuzeichnen des Overlays

            #return QPointF(nx, ny)
            return value

        return super().itemChange(change, value)


class DimOverlay(QGraphicsItem):
    def __init__(self, target_box: 'AspectBox'):
        super().__init__()
        self.target_box = target_box
        self.setZValue(-1)  # Hinter der Box, aber über dem PDF
        # Sorgt dafür, dass das Overlay nicht klickbar ist
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemHasNoContents, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

    def boundingRect(self):
        # Das Overlay deckt die gesamte PDF-Seite ab
        if self.scene():
            return self.scene().sceneRect()
        return QRectF()

    def paint(self, painter, option, widget):
        if not self.scene():
            return

        # 1. Gesamte Fläche der Szene
        path = QPainterPath()
        path.addRect(self.scene().sceneRect())

        # 2. Den Bereich der Boundingbox abziehen
        # Wir transformieren die Box-Koordinaten in Scene-Koordinaten
        box_rect = self.target_box.sceneBoundingRect()
        path.addRect(box_rect)

        # 3. Zeichnen mit dem 'OddEvenFill'-Loch-Effekt
        painter.setBrush(QBrush(QColor(0, 0, 0, 150))) # Halbtransparentes Schwarz
        painter.setPen(Qt.PenStyle.NoPen)
        # Nutzt OddEvenFill, damit das innere Rechteck transparent bleibt
        path.setFillRule(Qt.FillRule.OddEvenFill)
        painter.drawPath(path)
