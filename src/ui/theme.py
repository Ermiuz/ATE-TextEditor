from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

def apply_theme(theme_name):
    palette = QPalette()
    if theme_name == "dark":
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    else:
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    QApplication.setPalette(palette)
