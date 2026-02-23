# repository.py
from typing import List

from sqlalchemy.orm import Session
from db.models import ShippingLabelType

class ShippingLabelRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self):
        return self.session.query(ShippingLabelType).all()

    def get_by_id(self, id: int):
        return self.session.query(ShippingLabelType).filter_by(id=id).first()

    def add(self, carrier, label_type, keywords):
        obj = ShippingLabelType(
            carrier=carrier,
            label_type=label_type,
            keywords=keywords
        )
        self.session.add(obj)
        self.session.commit()

    def update(self, id, carrier, label_type, keywords):
        obj = self.get_by_id(id)
        if obj:
            obj.carrier = carrier
            obj.label_type = label_type
            obj.keywords = keywords
            self.session.commit()

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()

    def get_all(self) -> list[type[ShippingLabelType]]:
        """
        Gibt eine Liste von ShippingLabelType-Instanzen zurück.
        """
        # .all() gibt Instanzen zurück, keine Typen.
        # Die Typ-Warnung rührt oft daher, wie die IDE die 'mapped' Klasse interpretiert.
        return self.session.query(ShippingLabelType).all()