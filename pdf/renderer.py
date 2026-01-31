import fitz
from PySide6.QtGui import QImage, QTransform


def render_pdf_page(path: str, zoom: float = 4.0):
    doc = fitz.open(path)
    page = doc[0]

    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    if pix.n == 3:
        fmt = QImage.Format_RGB888
    else:
        fmt = QImage.Format_RGBA8888

    image = QImage(
        pix.samples,
        pix.width,
        pix.height,
        pix.stride,
        fmt
    ).copy()

    # WICHTIG:
    # KEINE Rotation hier!
    rotated = False

    return image, page.rect, rotated