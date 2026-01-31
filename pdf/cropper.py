import fitz  # PyMuPDF


import fitz

def widget_rect_to_pdf_rect(widget_rect, pdf_page, view_width, view_height):
    page_width = pdf_page.rect.width
    page_height = pdf_page.rect.height
    rotation = pdf_page.rotation

    scale_x = page_width / view_width
    scale_y = page_height / view_height

    x0 = widget_rect.left() * scale_x
    y0 = widget_rect.top() * scale_y
    x1 = widget_rect.right() * scale_x
    y1 = widget_rect.bottom() * scale_y

    rect = fitz.Rect(x0, y0, x1, y1)

    # Rotation korrigieren
    if rotation == 90:
        rect = fitz.Rect(
            y0,
            page_width - x1,
            y1,
            page_width - x0
        )
    elif rotation == 180:
        rect = fitz.Rect(
            page_width - x1,
            page_height - y1,
            page_width - x0,
            page_height - y0
        )
    elif rotation == 270:
        rect = fitz.Rect(
            page_height - y1,
            x0,
            page_height - y0,
            x1
        )

    return rect


def crop_pdf(input_path, output_path, pdf_rect):
    doc = fitz.open(input_path)
    page = doc[0]
    page.set_cropbox(pdf_rect)
    doc.save(output_path)
    doc.close()