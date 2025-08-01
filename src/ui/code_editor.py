# ui/code_editor.py
from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt6.QtGui import QPainter, QColor, QTextFormat, QFont
from PyQt6.QtCore import Qt, QRect

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setFont(editor.font())

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.setFont(QFont("Consolas", 12))
        
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#3e3d32"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#B0A782"))
                # Crea un QRect per il numero di linea
                rect = QRect(0, top, self.lineNumberArea.width() - 5, int(self.fontMetrics().height()))
                painter.drawText(rect, Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1


    def highlightCurrentLine(self):
        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        
        lineColor = QColor("#FFF2BD").lighter(120)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        
        self.setExtraSelections(extraSelections)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        cursor = self.cursorForPosition(event.pos())
        self.highlightLineUnderMouse(cursor)

    def highlightLineUnderMouse(self, cursor):
        extraSelections = self.extraSelections()
        if len(extraSelections) > 1:  # Conserva evidenziazione corrente
            extraSelections = extraSelections[:1]
            
        selection = QTextEdit.ExtraSelection()
        hoverColor = QColor(72, 72, 74)  # Colore più scuro per hover
        selection.format.setBackground(hoverColor)
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = cursor
        selection.cursor.clearSelection()
        
        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
