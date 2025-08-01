from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import QRegularExpression

class Highlighter(QSyntaxHighlighter):
    def __init__(self, document, file_format):
        super().__init__(document)
        self.highlight_rules = []
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QTextCharFormat.FontWeight.Bold)
        keywords = ["def", "class", "return", "import", "from", "as"]
        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}\b")
            self.highlight_rules.append((pattern, keyword_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlight_rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
