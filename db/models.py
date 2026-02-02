from dataclasses import dataclass

# -----------------------------
# Paper Format (paper_formats)
# -----------------------------
@dataclass
class PaperFormat:
    id: int
    name: str
    width_mm: float
    height_mm: float


# -----------------------------
# Shipping Label Type (ShippingLabelType_definitions)
# -----------------------------
@dataclass
class ShippingLabelType:
    id: int
    carrier: str
    label_type: str
    keywords: str
    format_id: int


# -----------------------------
# Crop Data (crop_data)
# -----------------------------
@dataclass
class CropData:
    id: int
    supplier_label_id: int
    paper_format_id: int
    crop_x0: float
    crop_y0: float
    crop_x1: float
    crop_y1: float
    rotation: int