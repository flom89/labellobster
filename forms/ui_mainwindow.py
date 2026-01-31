# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowKMVdHI.ui'
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
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1600, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pdfContainer = QFrame(self.centralwidget)
        self.pdfContainer.setObjectName(u"pdfContainer")
        self.pdfContainer.setGeometry(QRect(414, 10, 1171, 720))
        self.pdfContainer.setFrameShape(QFrame.Shape.StyledPanel)
        self.pdfContainer.setFrameShadow(QFrame.Shadow.Raised)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 20, 391, 171))
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 40, 361, 50))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.widget)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.widget1 = QWidget(self.centralwidget)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(10, 200, 273, 28))
        self.horizontalLayout = QHBoxLayout(self.widget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btnOpenFile = QPushButton(self.widget1)
        self.btnOpenFile.setObjectName(u"btnOpenFile")

        self.horizontalLayout.addWidget(self.btnOpenFile)

        self.btnGenerate = QPushButton(self.widget1)
        self.btnGenerate.setObjectName(u"btnGenerate")

        self.horizontalLayout.addWidget(self.btnGenerate)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1600, 33))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Label Lobster", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Print Settings", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Target Label Format", None))
        self.btnOpenFile.setText(QCoreApplication.translate("MainWindow", u"Load Original Label", None))
        self.btnGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate Printable Label", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
    # retranslateUi

