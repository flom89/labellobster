# models.py
from sqlalchemy.orm import registry, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

mapper_registry = registry()


@mapper_registry.mapped
class ShippingLabelType:
    __tablename__ = "shipping_label_type"

    id = Column(Integer, primary_key=True)
    carrier = Column(String)
    label_type = Column(String)
    keywords = Column(String)

    crops = relationship("CropData", back_populates="label")


@mapper_registry.mapped
class CropData:
    __tablename__ = "crop_data"

    id = Column(Integer, primary_key=True)
    supplier_label_id = Column(Integer, ForeignKey("shipping_label_type.id"))

    printer_name = Column(String)
    paper_format_name = Column(String)

    crop_x0 = Column(Float)
    crop_y0 = Column(Float)
    crop_x1 = Column(Float)
    crop_y1 = Column(Float)
    rotation = Column(Integer)

    label = relationship("ShippingLabelType", back_populates="crops")