from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from forms.ui_SupplierLabelManager import Ui_SupplierLabelManager


class SupplierLabelManager(QDialog):
    def __init__(self, def_db, format_db, parent=None):
        super().__init__(parent)

        self.ui = Ui_SupplierLabelManager()
        self.ui.setupUi(self)

        self.def_db = def_db
        self.format_db = format_db
        self.current_id = None

        # Carrier-Liste füllen
        self._load_carriers()

        # Format-Liste füllen
        self._load_formats()

        # Tabelle füllen
        self._load_data()

        # Signale verbinden
        self.ui.btnNew.clicked.connect(self._new)
        self.ui.btnSave.clicked.connect(self._save)
        self.ui.btnDelete.clicked.connect(self._delete)
        self.ui.btnClose.clicked.connect(self.accept)

        self.ui.tableDefinitions.cellClicked.connect(self._on_row_selected)

    # ---------------------------------------------------------
    # Carrier-Liste
    # ---------------------------------------------------------
    def _load_carriers(self):
        carriers = [
            "DHL",
            "DPD",
            "UPS",
            "Hermes",
            "GLS",
            "FedEx",
            "Sonstige"
        ]
        self.ui.comboCarrier.clear()
        self.ui.comboCarrier.addItems(carriers)

    # ---------------------------------------------------------
    # Format-Liste
    # ---------------------------------------------------------
    def _load_formats(self):
        self.ui.comboFormat.clear()
        formats = self.format_db.list_all()

        for fmt in formats:
            label = f"{fmt.name} ({fmt.width_mm}×{fmt.height_mm})"
            self.ui.comboFormat.addItem(label, fmt.id)

    # ---------------------------------------------------------
    # Tabelle laden
    # ---------------------------------------------------------
    def _load_data(self):
        rows = self.def_db.list_all()
        table = self.ui.tableDefinitions
        table.setRowCount(len(rows))

        for row_idx, row in enumerate(rows):
            item_carrier = QTableWidgetItem(row["carrier"])
            item_carrier.setData(1000, row["id"])

            table.setItem(row_idx, 0, item_carrier)
            table.setItem(row_idx, 1, QTableWidgetItem(row["label_type"]))
            table.setItem(row_idx, 2, QTableWidgetItem(row["keywords"]))

    # ---------------------------------------------------------
    # Zeile ausgewählt
    # ---------------------------------------------------------
    def _on_row_selected(self, row, col):
        table = self.ui.tableDefinitions
        item = table.item(row, 0)
        if not item:
            return

        id = item.data(1000)
        entry = self.def_db.get_by_id(id)
        if not entry:
            return

        self.current_id = id

        self.ui.comboCarrier.setCurrentText(entry["carrier"])
        self.ui.editLabelType.setText(entry["label_type"])
        self.ui.editKeywords.setText(entry["keywords"])

        # Format auswählen
        idx = self.ui.comboFormat.findData(entry["format_id"])
        if idx >= 0:
            self.ui.comboFormat.setCurrentIndex(idx)

    # ---------------------------------------------------------
    # Neu
    # ---------------------------------------------------------
    def _new(self):
        self.current_id = None
        self.ui.comboCarrier.setCurrentIndex(0)
        self.ui.editLabelType.clear()
        self.ui.editKeywords.clear()
        self.ui.comboFormat.setCurrentIndex(0)
        self.ui.tableDefinitions.clearSelection()

    # ---------------------------------------------------------
    # Speichern
    # ---------------------------------------------------------
    def _save(self):
        carrier = self.ui.comboCarrier.currentText()
        label_type = self.ui.editLabelType.text().strip()
        keywords = self.ui.editKeywords.text().strip()
        format_id = self.ui.comboFormat.currentData()

        if not carrier or not label_type or not keywords:
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen.")
            return

        if self.current_id is None:
            self.def_db.add(carrier, label_type, keywords, format_id)
        else:
            self.def_db.update(self.current_id, carrier, label_type, keywords, format_id)

        self._load_data()
        self._new()

    # ---------------------------------------------------------
    # Löschen
    # ---------------------------------------------------------
    def _delete(self):
        if self.current_id is None:
            return

        self.def_db.delete(self.current_id)
        self._load_data()
        self._new()