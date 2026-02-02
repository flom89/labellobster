from PySide6.QtWidgets import QApplication
import qt_themes
from windows.main_window import MainWindow
import sys
from PySide6 import QtWidgets
from qt_material import apply_stylesheet

if __name__ == "__main__":

    app = QtWidgets.QApplication()
    qt_themes.set_theme('one_dark_two')
    window = MainWindow()
    window.show()
    app.exec()