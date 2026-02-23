import qt_themes
from PySide6 import QtWidgets

from windows.main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qt_themes.set_theme('one_dark_two')
    window = MainWindow()
    window.show()
    app.exec()
