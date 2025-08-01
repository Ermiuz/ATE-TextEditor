import PyQt6 
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication
import sys
from ui.main_window import TextEditor

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())
