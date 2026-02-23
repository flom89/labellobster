import fitz
from PySide6.QtCore import QSettings, QEvent
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QFileDialog, QGraphicsScene
)
from PySide6.QtWidgets import QMessageBox, QFrame

from db.CropDataRepository import CropDataRepository
from db.ShippingLabelRepository import ShippingLabelRepository
from db.database import get_session
from forms.ui_mainwindow import Ui_MainWindow
from modules.print import PrintingSystem
from pdf_renderer import PDFRenderer
from widgets.widgets import AspectBox, DimOverlay
from windows.SupplierLabelManager import SupplierLabelManager


class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung."""

    def __init__(self):
        super().__init__()

        # ---------------------------------------------------------
        # Objektive und Variablen
        # ---------------------------------------------------------
        # Initialisierung des PPF Viewer Objekts muss ganz am Anfang erfolgen
        self.current_target_ratio = None
        self.dim_overlay = None
        #self.pdf_viewer = PdfViewer(self)
        self.current_pdf_path = None
        self.PrintSystem = PrintingSystem()
        self.user_settings = QSettings("LabelLobster", "UserSettings")

        # ---------------------------------------------------------
        # Datenbank
        # ---------------------------------------------------------
        self.session = get_session()
        self.crop_repo = CropDataRepository(self.session)
        self.label_repo = ShippingLabelRepository(self.session)

        # ---------------------------------------------------------
        # Initialisierung der GUI
        # ---------------------------------------------------------
        # Initialisierung UserInterface
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scene = QGraphicsScene(self)
        self.ui.graphicsViewImportedLabel.setScene(self.scene)

        # Daten für das UI Laden
        self.read_printer_information_from_system()
        self.load_data_for_shipping_label_selector()
        self.set_last_user_settings_for_printer()

        self.scene = QGraphicsScene(self)
        self.ui.graphicsViewImportedLabel.setScene(self.scene)

        self.renderer = None
        self.pixmap_item = None
        self.crop_box = None
        self.pdf_original_rect = None

        # ---------------------------------------------------------
        # Events verbinden
        # ---------------------------------------------------------
        self.ui.btnPrint.clicked.connect(self.on_print_button_clicked)
        self.ui.cmbPrinterSlection.currentIndexChanged.connect(self.on_printer_settings_changed)
        self.ui.cmbPrinterPaperSelection.currentIndexChanged.connect(self.on_printer_paper_settings_changed)
        self.ui.btnSaveCrop.clicked.connect(self.on_save_crop_clicked)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionImportShippingSlip.triggered.connect(self.import_pdf_from_file)
        self.ui.actionShowSupplierLabelManager.triggered.connect(self.show_supplier_label_manager)
        self.ui.graphicsViewImportedLabel.viewport().installEventFilter(self)
        self.ui.cmbPrinterSlection.currentTextChanged.connect(self.update_crop_box_ratio)
        self.ui.cmbPrinterPaperSelection.currentTextChanged.connect(self.update_crop_box_ratio)

        self.update_crop_box_ratio()



    def show_supplier_label_manager(self):
        dlg = SupplierLabelManager(self.label_repo)
        dlg.exec()
        self.load_data_for_shipping_label_selector()

    def load_data_for_shipping_label_selector(self):
        combo = self.ui.cmbShippingLabelType
        combo.clear()

        for row in self.label_repo.list_all():
            label = f"{row.carrier} – {row.label_type}"
            self.ui.cmbShippingLabelType.addItem(label, row.id)

    # ---------------------------------------------------------
    # Druckerdaten laden zum Programmstart
    # ---------------------------------------------------------
    def read_printer_information_from_system(self):
        printers = self.PrintSystem.get_available_printers()
        for printer in printers:
            self.ui.cmbPrinterSlection.addItem(printer.printerName())

    # ---------------------------------------------------------
    # Userdaten laden Drucker und Druckerauswahl
    # ---------------------------------------------------------
    # Letzten eingestellten Drucker wieder setzen
    def set_last_user_settings_for_printer(self):
        last_text = self.user_settings.value("ui/printer_selection", "")
        index = self.ui.cmbPrinterSlection.findText(last_text)
        if index >= 0:
            self.ui.cmbPrinterSlection.setCurrentIndex(index)
            self.set_last_user_settings_for_paper()

    # ---------------------------------------------------------
    # Letztes eingestelltes Papier wieder setzen
    # ---------------------------------------------------------
    def set_last_user_settings_for_paper(self):

        # Verfügbare Papiere ermitteln
        available_papers = self.PrintSystem.load_paper_formats()

        # ComboBox leeren
        self.ui.cmbPrinterPaperSelection.clear()

        # Papierformate korrekt einfügen (Name + QPageSize als UserData)
        for ps in available_papers:
            self.ui.cmbPrinterPaperSelection.addItem(ps.name(), ps)

        # Abgleich mit gespeichertem letztem verwendeten Stand
        last_paper = self.user_settings.value("ui/paper_selection", "")
        index = self.ui.cmbPrinterPaperSelection.findText(last_paper)

        if index >= 0:
            self.ui.cmbPrinterPaperSelection.setCurrentIndex(index)
            self.get_paper_detailed_information()

    # ---------------------------------------------------------
    # Event Handler for Change of Printer Selection
    # ---------------------------------------------------------
    def on_printer_settings_changed(self):
        # Drucker setzen
        self.PrintSystem.printer.setPrinterName(self.ui.cmbPrinterSlection.currentText())

        # Verfügbare Papiere ermitteln
        available_papers = self.PrintSystem.load_paper_formats()

        # ComboBox leeren
        self.ui.cmbPrinterPaperSelection.clear()

        # Papierformate einfügen: Name als Text, QPageSize als UserData
        for ps in available_papers:
            self.ui.cmbPrinterPaperSelection.addItem(ps.name(), ps)

        self.save_selected_printer()

    # ---------------------------------------------------------
    # Event Handler for Change of Selected Paper
    # ---------------------------------------------------------
    def on_printer_paper_settings_changed(self):
        ps = self.ui.cmbPrinterPaperSelection.currentData()

        self.PrintSystem.printer.setPageSize(ps)

        self.save_selected_paper()
        self.get_paper_detailed_information()
        return

    # ---------------------------------------------------------
    # Get Paper Size Information for GUI and Ratio
    # ---------------------------------------------------------
    def get_paper_detailed_information(self):
        paper_info = self.PrintSystem.get_selected_paper_information()

        size_pt = paper_info.sizePoints()
        w = size_pt.width()
        h = size_pt.height()

        label = f"{int(w)}x{int(h)}"
        ratio = w / h

        self.ui.lblLabelSize.setText(f"{int(w)}x{int(h)} pt")
        self.ui.lblRatio.setText(f"{float(ratio):.2f}")

        return

    # ---------------------------------------------------------
    # Save Printer and Paper Selection
    # ---------------------------------------------------------
    def save_selected_printer(self):
        self.user_settings.setValue("ui/printer_selection", self.ui.cmbPrinterSlection.currentText())

    def save_selected_paper(self):
        self.user_settings.setValue("ui/paper_selection", self.ui.cmbPrinterPaperSelection.currentText())

    # ---------------------------------------------------------
    # Identify Label Types
    # ---------------------------------------------------------
    def identify_label_type(self) -> int | None:
        """
        Durchsucht den PDF-Text nach Keywords und gibt die ID des Labeltyps zurück.
        """
        # 1. Text extrahieren
        raw_text = self.renderer.get_page_text(0)
        if not raw_text:
            print("DEBUG: PDF enthält keinen extrahierbaren Text (eventuell ein Scan/Bild).")
            return None

        pdf_text = raw_text.lower()

        # 2. Alle Label-Typen aus der DB holen
        label_types = self.label_repo.get_all()

        # 3. Keyword-Abgleich
        for l_type in label_types:
            if not l_type.keywords:
                continue

            # Keywords säubern und in Liste wandeln
            keywords = [k.strip().lower() for k in l_type.keywords.split(",") if k.strip()]

            # Wenn ein Keyword im PDF-Text vorkommt -> Treffer!
            for kw in keywords:
                if kw in pdf_text:
                    print(f"DEBUG: Label identifiziert als: {l_type.carrier} {l_type.label_type} (ID: {l_type.id})")
                    return l_type.id

        print("DEBUG: Kein passendes Label für diesen PDF-Text in der Datenbank gefunden.")
        return None

    def update_crop_box_ratio(self):
        if not hasattr(self, 'PrintSystem'): return

        printer_name = self.ui.cmbPrinterSlection.currentText()
        self.PrintSystem.set_printer(printer_name)

        # 1. Ratio vom Drucker abfragen (berücksichtigt Orientierung)
        new_ratio = self.PrintSystem.get_current_paper_ratio()

        # 2. Validierung
        self.current_target_ratio = new_ratio if new_ratio > 0 else 1.5

        # 3. GUI Update
        if hasattr(self, 'crop_box') and self.crop_box is not None:
            self.crop_box.set_ratio(self.current_target_ratio)
            print(f"DEBUG: Box auf {self.current_target_ratio:.2f} gesetzt.")

    # ---------------------------------------------------------
    # Datei öffnen
    # ---------------------------------------------------------
    def import_pdf_from_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "PDF öffnen", "", "PDF Dateien (*.pdf)"
        )
        if not file_path:
            return

        self.current_pdf_path = file_path

        # 1. Daten laden & Scene bereinigen
        self.scene.clear()
        self.renderer = PDFRenderer(file_path)
        pixmap, self.pdf_original_rect = self.renderer.get_page_pixmap(0, dpi=200)

        # 2. Pixmap Item erstellen & Scene-Größe fixieren
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.pixmap_item.setZValue(-2)
        img_rect = self.pixmap_item.boundingRect()
        self.scene.setSceneRect(img_rect)

        # 3. Box & Overlay initialisieren (Standard-Position)
        ratio = getattr(self, 'current_target_ratio', 1.5)
        if not ratio or ratio <= 0: ratio = 1.5

        box_w = img_rect.width() * 0.6
        self.crop_box = AspectBox(0, 0, ratio)
        self.crop_box.set_size_by_width(box_w)

        # Initiale Zentrierung (Fallback)
        self.crop_box.setPos((img_rect.width() - box_w) / 2, (img_rect.height() - (box_w / ratio)) / 2)

        self.scene.addItem(self.crop_box)
        self.dim_overlay = DimOverlay(self.crop_box)
        self.dim_overlay.setZValue(-1)
        self.scene.addItem(self.dim_overlay)

        self.update_view_scale()

        # --- AUTOMATISIERUNG MIT POPUP-LOGIK ---

        detected_id = self.identify_label_type()
        if detected_id:
            # 1. Alle verfügbaren Konfigurationen für dieses Label aus der DB holen
            all_crops = self.crop_repo.get_all_by_label_id(detected_id)

            # Aktuelle UI-Einstellung (Was hat der User gerade eingestellt?)
            current_printer = self.ui.cmbPrinterSlection.currentText()
            current_paper = self.ui.cmbPrinterPaperSelection.currentText()

            # 2. Schritt: Suchen wir einen EXAKTEN Treffer für die aktuelle Hardware
            exact_match = next((c for c in all_crops if c.printer_name == current_printer
                                and c.paper_format_name == current_paper), None)

            if exact_match:
                # Fall A: Wir haben genau für diesen Drucker/Papier schon einen Crop!
                # Kein Popup nötig.
                self.load_crop(detected_id, current_paper, current_printer)
                # Update GUI
                self.set_label_combo_by_id(exact_match.supplier_label_id)

                #print("DEBUG: Exakter Hardware-Match gefunden. Lade Box...")

            elif len(all_crops) > 0:
                # Fall B: Wir haben zwar Crops für DHL, aber NICHT für die aktuelle Hardware
                # JETZT muss das Popup erscheinen, damit der User wählen kann:
                # "Willst du eine der vorhandenen Boxen (z.B. vom anderen Drucker) nutzen?"
                selected_row = self.show_crop_selection_dialog(all_crops)

                if selected_row:
                    # UI anpassen (Drucker/Papier auf den gewählten Crop umstellen)
                    self.ui.cmbPrinterSlection.setCurrentText(selected_row.printer_name)
                    self.ui.cmbPrinterPaperSelection.setCurrentText(selected_row.paper_format_name)
                    self.load_crop(detected_id, selected_row.paper_format_name, selected_row.printer_name)
            else:
                # Fall C: Label erkannt, aber noch nie ein Crop dafür gespeichert
                print("DEBUG: Neues Label ohne gespeicherte Boxen.")
                # Standard-Zentrierung der Box bleibt aktiv

    def mousePressEvent(self, event):
        # 1. Prüfen, ob es ein Rechtsklick war
        if event.button() == Qt.MouseButton.RightButton:
            self.reset_crop_box()
            event.accept()  # Verhindert, dass das Event weitergereicht wird
        else:
            # Wichtig: Linksklick (Verschieben der Box) normal erlauben
            super().mousePressEvent(event)

    def reset_crop_box(self):
        # Falls deine View in der Main z.B. 'view' oder 'graphicsView' heißt:
        view = self.ui.graphicsViewImportedLabel  # <- Hier den Namen deiner View-Variable nutzen

        if hasattr(self, 'crop_box') and self.crop_box:
            # 1. Logik-Reset auf 100x100 (Quadrat)
            self.crop_box.ratio = 1.0
            new_size = 100.0
            self.crop_box.setRect(0, 0, new_size, new_size)

            # 2. Lücke füllen: Zentrum der VIEW in SCENE-Koordinaten umrechnen
            # Wir nehmen das Rechteck des Sichtbereichs (Viewport)
            view_rect = view.viewport().rect()

            # Wir nehmen die Mitte dieses Rechtecks (Pixel-Koordinaten)
            view_center_pixel = view_rect.center()

            # Wir mappen diese Pixel-Mitte in die Koordinaten der Zeichenfläche (Scene)
            scene_center = view.mapToScene(view_center_pixel)

            # 3. Box positionieren (Zentrum minus halbe Box-Breite/-Höhe)
            self.crop_box.setPos(scene_center.x() - (new_size / 2),
                                 scene_center.y() - (new_size / 2))

            # 4. Handle-Grafik der Box aktualisieren
            if hasattr(self.crop_box, 'update_handle_visuals'):
                self.crop_box.update_handle_visuals()

            self.crop_box.update()

    def show_crop_selection_dialog(self, crops):
        """Zeigt ein Auswahl-Popup für mehrere Boundingboxen."""
        # Anzeige-Strings erstellen
        options = [f"Drucker: {c.printer_name} | Papier: {c.paper_format_name}" for c in crops]

        from PySide6.QtWidgets import QInputDialog
        item, ok = QInputDialog.getItem(
            self, "Konfiguration wählen",
            "Mehrere Boxen für dieses Label gefunden:",
            options, 0, False
        )

        if ok and item:
            index = options.index(item)
            return crops[index]
        return None

    def set_label_combo_by_id(self, label_id: int):
        # findData sucht den Index, an dem die ID im Hintergrund (UserData) steckt
        index = self.ui.cmbShippingLabelType.findData(label_id)
        if index >= 0:
            self.ui.cmbShippingLabelType.setCurrentIndex(index)

    def update_view_scale(self) -> None:
        view = self.ui.graphicsViewImportedLabel

        # 1. Validierung: Existiert das Item und ist es in der Scene?
        if not hasattr(self, 'pixmap_item') or self.pixmap_item is None:
            return
        if self.pixmap_item.scene() is None:
            return

        # 2. Geometrie-Abgleich
        # Wir nehmen die Größe des Viewports (die echte Zeichenfläche)
        v_size = view.viewport().size()
        if v_size.width() <= 10 or v_size.height() <= 10:
            return

        # 3. Scene-Begrenzung fixieren (WICHTIG!)
        # Wenn die SceneRect nicht exakt dem PDF entspricht, scheitert fitInView
        img_rect = self.pixmap_item.boundingRect()
        view.scene().setSceneRect(img_rect)

        # 4. Scrollbars & Rahmen deaktivieren (verhindert Rand-Artefakte)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setFrameShape(QFrame.Shape.NoFrame)

        # 5. Die Skalierung erzwingen
        # fitInView berechnet die Matrix basierend auf v_size und img_rect
        view.fitInView(img_rect, Qt.AspectRatioMode.KeepAspectRatio)

        # Optional: Debug-Check (Sollte jetzt deutlich über 0.0103 liegen)
        # print(f"DEBUG: Neue Skalierung: {view.transform().m11():.4f}")

    def eventFilter(self, source, event) -> bool:
        # Wir lauschen auf den Viewport der GraphicsView
        if source is self.ui.graphicsViewImportedLabel.viewport():
            if event.type() == QEvent.Type.Resize:
                # Das Layout hat der View eine neue Größe gegeben
                # Wir rufen die Skalierung auf
                self.update_view_scale()
        return super().eventFilter(source, event)

    # ---------------------------------------------------------
    # PDF Koordinaten ermitteln
    # ---------------------------------------------------------
    def get_pdf_coordinates(self) -> dict:
        if not self.renderer or not self.crop_box or not self.pixmap_item:
            return {}

        # 1. Skalierung (GUI-Pixel zu PDF-Punkten)
        pixmap_rect = self.pixmap_item.boundingRect()
        pdf_rect = self.pdf_original_rect  # 72 DPI

        scale_x = pdf_rect.width / pixmap_rect.width()
        scale_y = pdf_rect.height / pixmap_rect.height()

        # 2. Box-Position (Scene-Koordinaten)
        # WICHTIG: Die Scene muss exakt die Größe des Pixmaps haben!
        box = self.crop_box.sceneBoundingRect()

        # 3. Validierung (Debug-Code einbauen!)
        x0 = box.left() * scale_x
        y0 = box.top() * scale_y
        w = box.width() * scale_x

        if x0 < -1 or w > (pdf_rect.width + 1):
            print(f"DEBUG_SAVE: [KRITISCH] Ungültige Werte! x0:{x0:.2f}, w:{w:.2f} (Limit: {pdf_rect.width})")
            # Hier merken wir: Die GUI-Daten sind zum Speichern noch nicht bereit!
        return {
            "x0": round(x0, 2),
            "y0": round(y0, 2),
            "x1": round((box.left() + box.width()) * scale_x, 2),
            "y1": round((box.top() + box.height()) * scale_y, 2),
            "width": round(w, 2),
            "height": round(box.height() * scale_y, 2)
        }

    # ---------------------------------------------------------
    # Crop speichern
    # ---------------------------------------------------------
    def on_save_crop_clicked(self):
        # 1. UI-Daten abrufen
        supplier_label_id = self.ui.cmbShippingLabelType.currentData()
        printer_name = self.ui.cmbPrinterSlection.currentText()
        paper_format_id = self.ui.cmbPrinterPaperSelection.currentText()

        # 2. Validierung: Sind die Metadaten vollständig?
        if not supplier_label_id or not paper_format_id or supplier_label_id == "Bitte wählen":
            QMessageBox.warning(self, "Eingabefehler",
                                "Bitte wählen Sie einen Label-Typ und ein Papierformat aus, bevor Sie speichern.")
            return

        # 3. Validierung: Ist überhaupt ein PDF geladen?
        if not hasattr(self, 'pixmap_item') or self.pixmap_item is None:
            QMessageBox.warning(self, "Kein PDF", "Es wurde kein PDF-Dokument zum Croppen geladen.")
            return

        # 4. Koordinaten abrufen
        pdf_coords = self.get_pdf_coordinates()

        # Check: Ist die Cropbox vielleicht 0x0 groß?
        if pdf_coords.get("width", 0) < 5 or pdf_coords.get("height", 0) < 5:
            QMessageBox.warning(self, "Ungültiger Ausschnitt",
                                "Der markierte Bereich ist zu klein. Bitte ziehen Sie eine gültige Box auf.")
            return

        # --- NEU: ROTATION ERMITTELN ---
        # Wir vergleichen das aktuelle Ratio der Box mit dem Basis-Ratio des Papiers.
        # Wenn sie abweichen, wurde die Box vom User "geflippt" (Quer statt Hoch).
        rotation_value = 0
        if hasattr(self, 'crop_box'):
            # Kleiner Toleranzbereich für Float-Vergleiche
            if abs(self.crop_box.ratio - self.crop_box.base_ratio) > 0.01:
                rotation_value = 90
                print(f"DEBUG_SAVE: Box ist geflippt. Speichere Rotation: {rotation_value}")

        # 4.5 Prüfung auf Duplikate
        existing_crop = self.crop_repo.get(supplier_label_id, paper_format_id, printer_name)

        if existing_crop:
            reply = QMessageBox.question(
                self,
                "Eintrag vorhanden",
                f"Für dieses Label auf '{paper_format_id}' existiert bereits eine Bounding-Box.\n\n"
                "Möchten Sie den bestehenden Eintrag überschreiben?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                return

        # 5. Speichervorgang
        try:
            self.crop_repo.add_or_update(
                supplier_label_id,
                printer_name,
                paper_format_id,
                pdf_coords["x0"],
                pdf_coords["y0"],
                pdf_coords["x1"],
                pdf_coords["y1"],
                rotation=rotation_value  # <--- Jetzt dynamisch
            )

            QMessageBox.information(self, "Erfolg",
                                    f"Bounding-Box wurde erfolgreich gespeichert (Rotation: {rotation_value}°).")

        except Exception as e:
            QMessageBox.critical(self, "Datenbankfehler",
                                 f"Die Box konnte nicht gespeichert werden.\nFehler: {str(e)}")



    # ---------------------------------------------------------
    # CROP laden
    # ---------------------------------------------------------
    def load_crop(self, supplier_label_id: int, paper_format_id: str, printer_name: str):
        # 1. Daten aus Repo holen
        row = self.crop_repo.get(supplier_label_id, paper_format_id, printer_name)
        if not row:
            return

        # 2. Skalierung berechnen (GUI / PDF-Punkte)
        pixmap_rect = self.pixmap_item.boundingRect()
        pdf_rect = self.pdf_original_rect
        scale_x = pixmap_rect.width() / pdf_rect.width
        scale_y = pixmap_rect.height() / pdf_rect.height

        # --- SCHRITT A: ROTATION / RATIO WIEDERHERSTELLEN ---
        if hasattr(self, 'crop_box'):
            # Wenn in der DB rotation=90 steht, muss die Box das invertierte Papier-Ratio nutzen
            if row.rotation == 90:
                # Wechsel zu Landscape (1 / Portrait-Ratio)
                self.crop_box.set_ratio(1.0 / self.crop_box.base_ratio)
            else:
                # Zurück zum Standard-Papierformat (Portrait)
                self.crop_box.set_ratio(self.crop_box.base_ratio)

        # --- SCHRITT B: POSITION UND GRÖSSE SETZEN ---
        # Erst nachdem das Ratio stimmt, berechnen wir die GUI-Pixel
        gui_x = row.crop_x0 * scale_x
        gui_y = row.crop_y0 * scale_y
        gui_w = (row.crop_x1 - row.crop_x0) * scale_x

        self.crop_box.setPos(gui_x, gui_y)
        self.crop_box.set_size_by_width(gui_w)

        # Overlay aktualisieren
        if hasattr(self, 'dim_overlay'):
            self.dim_overlay.update()

        #print(f"DEBUG: Crop geladen (Rotation: {row.rotation}°, Ratio: {self.crop_box.ratio:.2f})")

    # ---------------------------------------------------------
    # Erstellen des gecroppten PDFs
    # ---------------------------------------------------------

    def create_cropped_pdf(self, source_pdf_path: str, output_pdf_path: str):
        if not self.renderer or not self.crop_box:
            return False

        coords = self.get_pdf_coordinates()

        try:
            # 1. Dokumente öffnen
            src_doc = fitz.open(source_pdf_path)

            # Sicherheits-Check: Hat das PDF überhaupt Seiten?
            if src_doc.page_count == 0:
                print("DEBUG: Quelldokument ist leer.")
                src_doc.close()
                return False

            # 2. Ziel-Dokument erstellen
            dest_doc = fitz.open()

            # 3. Das Rechteck für den Ausschnitt (72 DPI)
            # Wir nutzen fitz.Rect direkt mit den berechneten Punkten
            crop_rect = fitz.Rect(
                coords["x0"], coords["y0"],
                coords["x1"], coords["y1"]
            )

            # 4. Neue Seite im Ziel-Dokument mit der Größe der Box anlegen
            dest_page = dest_doc.new_page(
                width=coords["width"],
                height=coords["height"]
            )

            # 5. Inhalt der Quellseite (Index 0) auf die Zielseite projizieren
            # WICHTIG: show_pdf_page braucht das Dokument-Objekt, nicht das Page-Objekt
            dest_page.show_pdf_page(
                dest_page.rect,  # Ziel-Rechteck (die ganze neue Seite)
                src_doc,  # Quelldokument
                pno=0,  # Seitennummer (0 = erste Seite)
                clip=crop_rect  # Der exakte Ausschnitt
            )

            # 6. Speichern (mit Kompression für den Drucker)
            dest_doc.save(output_pdf_path, garbage=3, deflate=True)

            dest_doc.close()
            src_doc.close()
            print(f"DEBUG: Crop erfolgreich erstellt: {output_pdf_path}")
            return True

        except Exception as e:
            print(f"DEBUG: Fehler beim PDF-Cropping: {str(e)}")
            return False

    # ---------------------------------------------------------
    # Drucken
    # ---------------------------------------------------------
    def on_print_button_clicked(self):
        temp_file = "to_print.pdf"

        # 1. Schritt: PDF anhand der Boundingbox croppen
        if self.create_cropped_pdf(self.current_pdf_path, temp_file):

            # 2. Schritt: Drucker konfigurieren
            printer_name = self.ui.cmbPrinterSlection.currentText()
            self.PrintSystem.set_printer(printer_name)

            # 3. Schritt: Drucken
            success = self.PrintSystem.print_pdf(temp_file)

            if success:
                print("Druckauftrag erfolgreich gesendet.")
