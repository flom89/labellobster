from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from forms.ui_PaperManager import Ui_PaperManager


class PaperManager(QDialog):
    def __init__(self, format_db, parent=None):
        super().__init__(parent)

        self.ui = Ui_PaperManager()
        self.ui.setupUi(self)

        self.format_db = format_db
        self.current_id = None

        # Signale verbinden
        self.ui.btnNew.clicked.connect(self._new_format)
        self.ui.btnSave.clicked.connect(self._save_format)
        self.ui.btnDelete.clicked.connect(self._delete_format)
        self.ui.btnClose.clicked.connect(self.accept)

        self.ui.tableFormats.cellClicked.connect(self._on_row_selected)

        self._load_data()

    # ---------------------------------------------------------
    # Daten laden
    # ---------------------------------------------------------
    def _load_data(self):
        formats = self.format_db.list_all()
        self.ui.tableFormats.setRowCount(len(formats))

        for row_idx, fmt in enumerate(formats):
            item_name = QTableWidgetItem(fmt.name)
            item_width = QTableWidgetItem(str(fmt.width_mm))
            item_height = QTableWidgetItem(str(fmt.height_mm))

            # ID speichern
            item_name.setData(1000, fmt.id)

            self.ui.tableFormats.setItem(row_idx, 0, item_name)
            self.ui.tableFormats.setItem(row_idx, 1, item_width)
            self.ui.tableFormats.setItem(row_idx, 2, item_height)

    # ---------------------------------------------------------
    # Tabellenzeile ausgewählt
    # ---------------------------------------------------------
    def _on_row_selected(self, row, col):
        item = self.ui.tableFormats.item(row, 0)
        if not item:
            return

        fmt_id = item.data(1000)
        fmt = self.format_db.get_by_id(fmt_id)
        if not fmt:
            return

        self.current_id = fmt.id
        self.ui.editName.setText(fmt.name)
        self.ui.editWidth.setText(str(fmt.width_mm))
        self.ui.editHeight.setText(str(fmt.height_mm))

    # ---------------------------------------------------------
    # Neues Format
    # ---------------------------------------------------------
    def _new_format(self):
        self.current_id = None
        self.ui.editName.clear()
        self.ui.editWidth.clear()
        self.ui.editHeight.clear()
        self.ui.tableFormats.clearSelection()

    # ---------------------------------------------------------
    # Speichern
    # ---------------------------------------------------------
    def _save_format(self):
        name = self.ui.editName.text().strip()

        try:
            width = float(self.ui.editWidth.text().replace(",", "."))
            height = float(self.ui.editHeight.text().replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Ungültige Eingabe", "Breite und Höhe müssen Zahlen sein.")
            return

        if not name:
            QMessageBox.warning(self, "Fehlender Name", "Bitte einen Namen angeben.")
            return

        if self.current_id is None:
            self.format_db.add(name, width, height)
        else:
            self.format_db.update(self.current_id, name, width, height)

        self._reload_after_change()

    # ---------------------------------------------------------
    # Löschen
    # ---------------------------------------------------------
    def _delete_format(self):
        if self.current_id is None:
            return

        self.format_db.delete(self.current_id)
        self._reload_after_change()

    # ---------------------------------------------------------
    # Nach Änderungen neu laden
    # ---------------------------------------------------------
    def _reload_after_change(self):
        self.current_id = None
        self.ui.editName.clear()
        self.ui.editWidth.clear()
        self.ui.editHeight.clear()
        self.ui.tableFormats.clearSelection()
        self._load_data()