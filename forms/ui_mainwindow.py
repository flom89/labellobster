# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowdwEiuK.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtGui import (QAction)
from PySide6.QtWidgets import (QComboBox, QGraphicsView, QGroupBox,
                               QHBoxLayout, QLabel, QMenu,
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
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.layoutGroup1.addWidget(self.label_2)

        self.cmbPrinterSlection = QComboBox(self.groupBox)
        self.cmbPrinterSlection.setObjectName(u"cmbPrinterSlection")
        self.cmbPrinterSlection.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.layoutGroup1.addWidget(self.cmbPrinterSlection)

        self.paper_format = QLabel(self.groupBox)
        self.paper_format.setObjectName(u"paper_format")

        self.layoutGroup1.addWidget(self.paper_format)

        self.cmbPrinterPaperSelection = QComboBox(self.groupBox)
        self.cmbPrinterPaperSelection.setObjectName(u"cmbPrinterPaperSelection")

        self.layoutGroup1.addWidget(self.cmbPrinterPaperSelection)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.layoutGroup1.addWidget(self.label)

        self.cmbShippingLabelType = QComboBox(self.groupBox)
        self.cmbShippingLabelType.setObjectName(u"cmbShippingLabelType")

        self.layoutGroup1.addWidget(self.cmbShippingLabelType)

        self.lblSizeLabel = QLabel(self.groupBox)
        self.lblSizeLabel.setObjectName(u"lblSizeLabel")

        self.layoutGroup1.addWidget(self.lblSizeLabel)

        self.lblLabelSize = QLabel(self.groupBox)
        self.lblLabelSize.setObjectName(u"lblLabelSize")

        self.layoutGroup1.addWidget(self.lblLabelSize)

        self.lblRatioLabel = QLabel(self.groupBox)
        self.lblRatioLabel.setObjectName(u"lblRatioLabel")

        self.layoutGroup1.addWidget(self.lblRatioLabel)

        self.lblRatio = QLabel(self.groupBox)
        self.lblRatio.setObjectName(u"lblRatio")

        self.layoutGroup1.addWidget(self.lblRatio)


        self.leftColumn.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.layoutGroup3 = QVBoxLayout(self.groupBox_3)
        self.layoutGroup3.setObjectName(u"layoutGroup3")
        self.btnSaveCrop = QPushButton(self.groupBox_3)
        self.btnSaveCrop.setObjectName(u"btnSaveCrop")

        self.layoutGroup3.addWidget(self.btnSaveCrop)


        self.leftColumn.addWidget(self.groupBox_3)

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


        self.leftColumn.addWidget(self.groupBox_4)

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
        self.graphicsViewImportedLabel = QGraphicsView(self.tab)
        self.graphicsViewImportedLabel.setObjectName(u"graphicsViewImportedLabel")

        self.tab1Layout.addWidget(self.graphicsViewImportedLabel)

        self.tabWidget.addTab(self.tab, "")

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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Druckerauswahl", None))
        self.paper_format.setText(QCoreApplication.translate("MainWindow", u"Drucker Papierformat", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Versandlabeltyp", None))
        self.lblSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Labelgr\u00f6\u00dfe", None))
        self.lblLabelSize.setText("")
        self.lblRatioLabel.setText(QCoreApplication.translate("MainWindow", u"Seitenverh\u00e4ltnis", None))
        self.lblRatio.setText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Automatik", None))
        self.btnSaveCrop.setText(QCoreApplication.translate("MainWindow", u"Als Standard Speichern", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Drucken", None))
        self.btnPrint.setText(QCoreApplication.translate("MainWindow", u"Drucken", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Originales Versandlabel", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuEinstellungen.setTitle(QCoreApplication.translate("MainWindow", u"Einstellungen", None))
    # retranslateUi

