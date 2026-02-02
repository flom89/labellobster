# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PaperManagerealnSx.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFormLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_PaperManager(object):
    def setupUi(self, PaperManager):
        if not PaperManager.objectName():
            PaperManager.setObjectName(u"PaperManager")
        PaperManager.resize(487, 246)
        self.verticalLayout_main = QVBoxLayout(PaperManager)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.horizontalLayout_center = QHBoxLayout()
        self.horizontalLayout_center.setObjectName(u"horizontalLayout_center")
        self.tableFormats = QTableWidget(PaperManager)
        if (self.tableFormats.columnCount() < 3):
            self.tableFormats.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableFormats.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableFormats.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableFormats.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableFormats.setObjectName(u"tableFormats")
        self.tableFormats.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableFormats.setAlternatingRowColors(True)
        self.tableFormats.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableFormats.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.horizontalLayout_center.addWidget(self.tableFormats)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(PaperManager)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelName)

        self.editName = QLineEdit(PaperManager)
        self.editName.setObjectName(u"editName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.editName)

        self.labelWidth = QLabel(PaperManager)
        self.labelWidth.setObjectName(u"labelWidth")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelWidth)

        self.editWidth = QLineEdit(PaperManager)
        self.editWidth.setObjectName(u"editWidth")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.editWidth)

        self.labelHeight = QLabel(PaperManager)
        self.labelHeight.setObjectName(u"labelHeight")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelHeight)

        self.editHeight = QLineEdit(PaperManager)
        self.editHeight.setObjectName(u"editHeight")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.editHeight)


        self.horizontalLayout_center.addLayout(self.formLayout)


        self.verticalLayout_main.addLayout(self.horizontalLayout_center)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.btnNew = QPushButton(PaperManager)
        self.btnNew.setObjectName(u"btnNew")

        self.horizontalLayout_buttons.addWidget(self.btnNew)

        self.btnSave = QPushButton(PaperManager)
        self.btnSave.setObjectName(u"btnSave")

        self.horizontalLayout_buttons.addWidget(self.btnSave)

        self.btnDelete = QPushButton(PaperManager)
        self.btnDelete.setObjectName(u"btnDelete")

        self.horizontalLayout_buttons.addWidget(self.btnDelete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer)

        self.btnClose = QPushButton(PaperManager)
        self.btnClose.setObjectName(u"btnClose")

        self.horizontalLayout_buttons.addWidget(self.btnClose)


        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)


        self.retranslateUi(PaperManager)

        QMetaObject.connectSlotsByName(PaperManager)
    # setupUi

    def retranslateUi(self, PaperManager):
        PaperManager.setWindowTitle(QCoreApplication.translate("PaperManager", u"Label-Formate verwalten", None))
        ___qtablewidgetitem = self.tableFormats.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PaperManager", u"Name", None));
        ___qtablewidgetitem1 = self.tableFormats.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PaperManager", u"Breite (mm)", None));
        ___qtablewidgetitem2 = self.tableFormats.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PaperManager", u"H\u00f6he (mm)", None));
        self.labelName.setText(QCoreApplication.translate("PaperManager", u"Name:", None))
        self.labelWidth.setText(QCoreApplication.translate("PaperManager", u"Breite (mm):", None))
        self.labelHeight.setText(QCoreApplication.translate("PaperManager", u"H\u00f6he (mm):", None))
        self.btnNew.setText(QCoreApplication.translate("PaperManager", u"Neu", None))
        self.btnSave.setText(QCoreApplication.translate("PaperManager", u"Speichern", None))
        self.btnDelete.setText(QCoreApplication.translate("PaperManager", u"L\u00f6schen", None))
        self.btnClose.setText(QCoreApplication.translate("PaperManager", u"Schlie\u00dfen", None))
    # retranslateUi

