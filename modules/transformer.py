import os
import time
import uuid
import tempfile
import fitz

from PySide6.QtCore import QRect, QPoint, QPointF
from PySide6.QtGui import QImage


class Transformer:
    def __init__(self, view, pixmap_item, pdf_image, pdf_rect, pdf_document, original_pdf_path):
        """
        view: QGraphicsView
        pixmap_item: QGraphicsPixmapItem (gerendertes PDF)
        pdf_image: QImage des gerenderten PDFs (für Breite/Höhe in Pixeln)
        pdf_rect: fitz.Rect der PDF-Seite (in PDF-Punkten)
        pdf_document: fitz.Document
        original_pdf_path: Pfad zur Original-PDF-Datei
        """
        self.view = view
        self.pixmap_item = pixmap_item
        self.pdf_image = pdf_image
        self.pdf_rect = pdf_rect
        self.pdf_document = pdf_document
        self.original_pdf_path = original_pdf_path

        # Logischer Seitenindex (für Mehrseiten-PDFs erweiterbar)
        self.page_index = 0
        # Rotation in Grad (falls du später echte PDF-Rotation einführen willst)
        self.rotation = 0

    # ---------------------------------------------------------
    # Overlay-Widget-Rect → PDF-Rect (in PDF-Koordinaten)
    # ---------------------------------------------------------
    def overlay_rect_to_pdf_rect(self, overlay, rect) -> fitz.Rect:
        if self.pixmap_item is None or self.pdf_rect is None:
            return None

        o_rect = rect

        p1_overlay = QPoint(o_rect.left(), o_rect.top())
        p2_overlay = QPoint(o_rect.right(), o_rect.bottom())

        # Overlay → Viewport
        p1_view = overlay.mapTo(self.view.viewport(), p1_overlay)
        p2_view = overlay.mapTo(self.view.viewport(), p2_overlay)

        # Viewport → Scene
        p1_scene = self.view.mapToScene(p1_view)
        p2_scene = self.view.mapToScene(p2_view)

        # Scene → PixmapItem (Rotation des Items wird von Qt berücksichtigt)
        p1_item = self.pixmap_item.mapFromScene(p1_scene)
        p2_item = self.pixmap_item.mapFromScene(p2_scene)

        pixmap = self.pixmap_item.pixmap()
        img_w = pixmap.width()
        img_h = pixmap.height()
        if img_w == 0 or img_h == 0:
            return None

        x0_img = max(0.0, min(img_w, p1_item.x()))
        y0_img = max(0.0, min(img_h, p1_item.y()))
        x1_img = max(0.0, min(img_w, p2_item.x()))
        y1_img = max(0.0, min(img_h, p2_item.y()))

        x0_img, x1_img = sorted([x0_img, x1_img])
        y0_img, y1_img = sorted([y0_img, y1_img])

        pdf_w = self.pdf_rect.width
        pdf_h = self.pdf_rect.height

        x0_pdf = x0_img / img_w * pdf_w
        x1_pdf = x1_img / img_w * pdf_w
        y0_pdf = y0_img / img_h * pdf_h
        y1_pdf = y1_img / img_h * pdf_h

        return fitz.Rect(x0_pdf, y0_pdf, x1_pdf, y1_pdf)

    # ---------------------------------------------------------
    # PDF-Rect → Preview-QImage (nur für Anzeige, Rasterisierung ok)
    # ---------------------------------------------------------
    def pdf_rect_to_preview_image(self, pdf_rect, dpi=200, page_index=None):
        if pdf_rect is None:
            return None

        if page_index is None:
            page_index = self.page_index

        page = self.pdf_document.load_page(page_index)
        pix = page.get_pixmap(clip=pdf_rect, dpi=dpi)

        if pix.alpha:
            fmt = QImage.Format_RGBA8888
        else:
            fmt = QImage.Format_RGB888

        img = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt).copy()
        return img

    # ---------------------------------------------------------
    # PDF-Rect → Cropped-PDF speichern (vektorbasiert)
    # ---------------------------------------------------------
    def save_cropped_pdf(self, pdf_rect, output_path, page_index=None):
        if pdf_rect is None:
            return

        if page_index is None:
            page_index = self.page_index

        src_doc = fitz.open(self.original_pdf_path)
        page = src_doc.load_page(0)

        # Neues PDF, das den Ausschnitt vektorbasiert referenziert
        new_doc = fitz.open()
        clip_w = pdf_rect.width
        clip_h = pdf_rect.height

        target_rect = fitz.Rect(0, 0, clip_w, clip_h)
        new_page = new_doc.new_page(width=clip_w, height=clip_h)

        new_page.show_pdf_page(
            target_rect,
            src_doc,
            page_number=page_index,
            clip=pdf_rect
        )

        def _do_save(tmp_path):
            new_doc.save(tmp_path)

        self.atomic_save(_do_save, output_path)

        new_doc.close()
        src_doc.close()

    # ---------------------------------------------------------
    # PDF-Rect → Overlay-Rect (zurück in Widget-Koordinaten)
    # ---------------------------------------------------------
    def pdf_rect_to_overlay_rect(self, overlay, pdf_rect) -> QRect:
        if pdf_rect is None or self.pixmap_item is None or self.pdf_rect is None:
            return QRect()

        pdf_w = self.pdf_rect.width
        pdf_h = self.pdf_rect.height

        pixmap = self.pixmap_item.pixmap()
        img_w = pixmap.width()
        img_h = pixmap.height()
        if img_w == 0 or img_h == 0:
            return QRect()

        x0_img = pdf_rect.x0 / pdf_w * img_w
        y0_img = pdf_rect.y0 / pdf_h * img_h
        x1_img = pdf_rect.x1 / pdf_w * img_w
        y1_img = pdf_rect.y1 / pdf_h * img_h

        p1_scene = self.pixmap_item.mapToScene(QPointF(x0_img, y0_img))
        p2_scene = self.pixmap_item.mapToScene(QPointF(x1_img, y1_img))

        p1_view = self.view.mapFromScene(p1_scene)
        p2_view = self.view.mapFromScene(p2_scene)

        p1_overlay = overlay.mapFrom(self.view.viewport(), p1_view)
        p2_overlay = overlay.mapFrom(self.view.viewport(), p2_view)

        x = int(min(p1_overlay.x(), p2_overlay.x()))
        y = int(min(p1_overlay.y(), p2_overlay.y()))
        w = int(abs(p2_overlay.x() - p1_overlay.x()))
        h = int(abs(p2_overlay.y() - p1_overlay.y()))

        return QRect(x, y, w, h)

    # ---------------------------------------------------------
    # Atomar speichern (für PDFs)
    # ---------------------------------------------------------
    @staticmethod
    def atomic_save(save_func, final_path, retries=10, delay=0.05):
        fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)

        for _ in range(retries):
            try:
                save_func(tmp_path)
                break
            except Exception:
                time.sleep(delay)
                delay *= 1.5
        else:
            raise RuntimeError(f"Could not save {final_path}: still locked")

        if os.path.exists(final_path):
            for _ in range(retries):
                try:
                    os.remove(final_path)
                    break
                except PermissionError:
                    time.sleep(0.05)
            # Wenn es immer noch da ist, lassen wir os.replace scheitern

        os.replace(tmp_path, final_path)

    # ---------------------------------------------------------
    # PDF-Rect → gerastertes Preview-Bild (für UI)
    # ---------------------------------------------------------
    def render_cropped_image(self, pdf_rect, page_index=None, dpi=200):
        if pdf_rect is None:
            return QImage()

        if page_index is None:
            page_index = self.page_index

        page = self.pdf_document.load_page(0)


        pix = page.get_pixmap(clip=pdf_rect, dpi=dpi)
        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888

        img = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            fmt
        ).copy()

        return img