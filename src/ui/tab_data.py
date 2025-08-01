from PyQt6.QtWidgets import QTextEdit

class TabData(QTextEdit):
    def __init__(self, file_format='.txt'):
        super().__init__()
        self._file_format = file_format

    @property
    def file_format(self):
        return self._file_format

    @file_format.setter
    def file_format(self, value):
        self._file_format = value if value.startswith('.') else f'.{value}'
