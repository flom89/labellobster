# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SupplierLabelManagerFKHCUs.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QFormLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_SupplierLabelManager(object):
    def setupUi(self, SupplierLabelManager):
        if not SupplierLabelManager.objectName():
            SupplierLabelManager.setObjectName(u"SupplierLabelManager")
        SupplierLabelManager.resize(908, 350)
        self.verticalLayout_main = QVBoxLayout(SupplierLabelManager)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.horizontalLayout_center = QHBoxLayout()
        self.horizontalLayout_center.setObjectName(u"horizontalLayout_center")
        self.tableDefinitions = QTableWidget(SupplierLabelManager)
        if (self.tableDefinitions.columnCount() < 3):
            self.tableDefinitions.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableDefinitions.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableDefinitions.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableDefinitions.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableDefinitions.setObjectName(u"tableDefinitions")
        self.tableDefinitions.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableDefinitions.setAlternatingRowColors(True)
        self.tableDefinitions.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableDefinitions.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableDefinitions.setColumnCount(3)
        self.tableDefinitions.horizontalHeader().setCascadingSectionResizes(False)
        self.tableDefinitions.horizontalHeader().setMinimumSectionSize(50)
        self.tableDefinitions.horizontalHeader().setDefaultSectionSize(135)
        self.tableDefinitions.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tableDefinitions.horizontalHeader().setStretchLastSection(False)

        self.horizontalLayout_center.addWidget(self.tableDefinitions)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelCarrier = QLabel(SupplierLabelManager)
        self.labelCarrier.setObjectName(u"labelCarrier")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCarrier)

        self.comboCarrier = QComboBox(SupplierLabelManager)
        self.comboCarrier.setObjectName(u"comboCarrier")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboCarrier)

        self.labelLabelType = QLabel(SupplierLabelManager)
        self.labelLabelType.setObjectName(u"labelLabelType")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelLabelType)

        self.editLabelType = QLineEdit(SupplierLabelManager)
        self.editLabelType.setObjectName(u"editLabelType")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.editLabelType)

        self.labelKeywords = QLabel(SupplierLabelManager)
        self.labelKeywords.setObjectName(u"labelKeywords")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelKeywords)

        self.editKeywords = QLineEdit(SupplierLabelManager)
        self.editKeywords.setObjectName(u"editKeywords")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.editKeywords)


        self.horizontalLayout_center.addLayout(self.formLayout)


        self.verticalLayout_main.addLayout(self.horizontalLayout_center)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.btnNew = QPushButton(SupplierLabelManager)
        self.btnNew.setObjectName(u"btnNew")

        self.horizontalLayout_buttons.addWidget(self.btnNew)

        self.btnSave = QPushButton(SupplierLabelManager)
        self.btnSave.setObjectName(u"btnSave")

        self.horizontalLayout_buttons.addWidget(self.btnSave)

        self.btnDelete = QPushButton(SupplierLabelManager)
        self.btnDelete.setObjectName(u"btnDelete")

        self.horizontalLayout_buttons.addWidget(self.btnDelete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer)

        self.btnClose = QPushButton(SupplierLabelManager)
        self.btnClose.setObjectName(u"btnClose")

        self.horizontalLayout_buttons.addWidget(self.btnClose)


        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)


        self.retranslateUi(SupplierLabelManager)

        QMetaObject.connectSlotsByName(SupplierLabelManager)
    # setupUi

    def retranslateUi(self, SupplierLabelManager):
        SupplierLabelManager.setWindowTitle(QCoreApplication.translate("SupplierLabelManager", u"Versandscheinmanager", None))
        ___qtablewidgetitem = self.tableDefinitions.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SupplierLabelManager", u"Logistikunternehmen", None));
        ___qtablewidgetitem1 = self.tableDefinitions.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SupplierLabelManager", u"Labeltyp", None));
        ___qtablewidgetitem2 = self.tableDefinitions.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SupplierLabelManager", u"Keywords", None));
        self.labelCarrier.setText(QCoreApplication.translate("SupplierLabelManager", u"Logistikunternehmen:", None))
        self.labelLabelType.setText(QCoreApplication.translate("SupplierLabelManager", u"Labeltyp:", None))
        self.labelKeywords.setText(QCoreApplication.translate("SupplierLabelManager", u"Keywords (kommagetrennt):", None))
        self.btnNew.setText(QCoreApplication.translate("SupplierLabelManager", u"Neu", None))
        self.btnSave.setText(QCoreApplication.translate("SupplierLabelManager", u"Speichern", None))
        self.btnDelete.setText(QCoreApplication.translate("SupplierLabelManager", u"L\u00f6schen", None))
        self.btnClose.setText(QCoreApplication.translate("SupplierLabelManager", u"Schlie\u00dfen", None))
    # retranslateUi

