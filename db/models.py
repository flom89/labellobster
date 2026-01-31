from dataclasses import dataclass

@dataclass
class LabelFormat:
    id: int
    name: str
    width_mm: float
    height_mm: float

@dataclass
class LabelCrop:
    id: int
    name: str
    pdf_width: float
    pdf_height: float
    crop_x0: float
    crop_y0: float
    crop_x1: float
    crop_y1: float
    rotation: int