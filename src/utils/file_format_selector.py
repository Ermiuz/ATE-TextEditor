from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton

class FileFormatSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleziona formato")
        layout = QVBoxLayout(self)

        label = QLabel("Scegli il formato del file:")
        layout.addWidget(label)

        self.combo = QComboBox(self)
        self.combo.addItems([".txt", ".py", ".java", ".js", ".html", ".css", ".json", ".md"])
        layout.addWidget(self.combo)

        ok_btn = QPushButton("OK", self)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

    def get_selected_format(self):
        return self.combo.currentText()
