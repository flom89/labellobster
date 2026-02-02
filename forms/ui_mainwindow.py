# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowgwtCkw.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 700)
        self.actionLabelmanager = QAction(MainWindow)
        self.actionLabelmanager.setObjectName(u"actionLabelmanager")
        self.actionShowPaperManager = QAction(MainWindow)
        self.actionShowPaperManager.setObjectName(u"actionShowPaperManager")
        self.actionShowSupplierLabelManager = QAction(MainWindow)
        self.actionShowSupplierLabelManager.setObjectName(u"actionShowSupplierLabelManager")
        self.actionImportShippingSlip = QAction(MainWindow)
        self.actionImportShippingSlip.setObjectName(u"actionImportShippingSlip")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.leftColumn = QVBoxLayout()
        self.leftColumn.setObjectName(u"leftColumn")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.layoutGroup1 = QVBoxLayout(self.groupBox)
        self.layoutGroup1.setObjectName(u"layoutGroup1")
        self.paper_format = QLabel(self.groupBox)
        self.paper_format.setObjectName(u"paper_format")

        self.layoutGroup1.addWidget(self.paper_format)

        self.cmbPaperType = QComboBox(self.groupBox)
        self.cmbPaperType.setObjectName(u"cmbPaperType")

        self.layoutGroup1.addWidget(self.cmbPaperType)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.layoutGroup1.addWidget(self.label)

        self.cmbShippingLabelType = QComboBox(self.groupBox)
        self.cmbShippingLabelType.setObjectName(u"cmbShippingLabelType")

        self.layoutGroup1.addWidget(self.cmbShippingLabelType)


        self.leftColumn.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.layoutGroup3 = QVBoxLayout(self.groupBox_3)
        self.layoutGroup3.setObjectName(u"layoutGroup3")
        self.btnSaveCrop = QPushButton(self.groupBox_3)
        self.btnSaveCrop.setObjectName(u"btnSaveCrop")

        self.layoutGroup3.addWidget(self.btnSaveCrop)

        self.btnAutoCrop = QPushButton(self.groupBox_3)
        self.btnAutoCrop.setObjectName(u"btnAutoCrop")

        self.layoutGroup3.addWidget(self.btnAutoCrop)


        self.leftColumn.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.layoutGroup2 = QVBoxLayout(self.groupBox_2)
        self.layoutGroup2.setObjectName(u"layoutGroup2")
        self.btnManualCrop = QPushButton(self.groupBox_2)
        self.btnManualCrop.setObjectName(u"btnManualCrop")

        self.layoutGroup2.addWidget(self.btnManualCrop)


        self.leftColumn.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnPrint = QPushButton(self.groupBox_4)
        self.btnPrint.setObjectName(u"btnPrint")

        self.verticalLayout.addWidget(self.btnPrint)

        self.btnPrintsettings = QPushButton(self.groupBox_4)
        self.btnPrintsettings.setObjectName(u"btnPrintsettings")

        self.verticalLayout.addWidget(self.btnPrintsettings)


        self.leftColumn.addWidget(self.groupBox_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftColumn.addItem(self.verticalSpacer_2)

        self.lblAutoDetectIndicator = QLabel(self.centralwidget)
        self.lblAutoDetectIndicator.setObjectName(u"lblAutoDetectIndicator")

        self.leftColumn.addWidget(self.lblAutoDetectIndicator)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftColumn.addItem(self.verticalSpacer)


        self.mainLayout.addLayout(self.leftColumn)

        self.rightColumn = QVBoxLayout()
        self.rightColumn.setObjectName(u"rightColumn")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab1Layout = QVBoxLayout(self.tab)
        self.tab1Layout.setObjectName(u"tab1Layout")
        self.pdfContainer = QFrame(self.tab)
        self.pdfContainer.setObjectName(u"pdfContainer")
        self.pdfContainer.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.pdfContainer.setFrameShape(QFrame.Shape.StyledPanel)

        self.tab1Layout.addWidget(self.pdfContainer)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab2Layout = QVBoxLayout(self.tab_2)
        self.tab2Layout.setObjectName(u"tab2Layout")
        self.pdfContainer_cropped = QFrame(self.tab_2)
        self.pdfContainer_cropped.setObjectName(u"pdfContainer_cropped")
        self.pdfContainer_cropped.setFrameShape(QFrame.Shape.StyledPanel)

        self.tab2Layout.addWidget(self.pdfContainer_cropped)

        self.tabWidget.addTab(self.tab_2, "")

        self.rightColumn.addWidget(self.tabWidget)


        self.mainLayout.addLayout(self.rightColumn)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 33))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuEinstellungen = QMenu(self.menubar)
        self.menuEinstellungen.setObjectName(u"menuEinstellungen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuEinstellungen.menuAction())
        self.menuDatei.addAction(self.actionImportShippingSlip)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionClose)
        self.menuEinstellungen.addAction(self.actionShowPaperManager)
        self.menuEinstellungen.addAction(self.actionShowSupplierLabelManager)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Label Lobster", None))
        self.actionLabelmanager.setText(QCoreApplication.translate("MainWindow", u"Labelmanager", None))
        self.actionShowPaperManager.setText(QCoreApplication.translate("MainWindow", u"Papierverwaltung anzeigen", None))
        self.actionShowSupplierLabelManager.setText(QCoreApplication.translate("MainWindow", u"Versandlabels konfigurieren", None))
        self.actionImportShippingSlip.setText(QCoreApplication.translate("MainWindow", u"Versandlabel importieren", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Beenden", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Drucken und Labelformat", None))
        self.paper_format.setText(QCoreApplication.translate("MainWindow", u"Papierformat", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Versandlabeltyp", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Automatik", None))
        self.btnSaveCrop.setText(QCoreApplication.translate("MainWindow", u"Als Standard Speichern", None))
        self.btnAutoCrop.setText(QCoreApplication.translate("MainWindow", u"Automatisches Beschneiden", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Manuel", None))
        self.btnManualCrop.setText(QCoreApplication.translate("MainWindow", u"Beschneiden", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Drucken", None))
        self.btnPrint.setText(QCoreApplication.translate("MainWindow", u"Drucken", None))
        self.btnPrintsettings.setText(QCoreApplication.translate("MainWindow", u"Druckeinstellungen", None))
        self.lblAutoDetectIndicator.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Originales Versandlabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Bearbeitetes Versandlabel", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuEinstellungen.setTitle(QCoreApplication.translate("MainWindow", u"Einstellungen", None))
    # retranslateUi

