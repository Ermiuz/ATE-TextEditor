from PyQt6.QtWidgets import QTextEdit, QInputDialog, QMessageBox

def find_text(editor: QTextEdit):
    """Trova il testo nel documento."""
    text, ok = QInputDialog.getText(editor, "Trova", "Inserisci il testo da cercare:")
    if ok and text:
        cursor = editor.textCursor()
        document = editor.document()
        found = document.find(text, cursor)
        if found.isNull():
            QMessageBox.information(editor, "Non trovato", f"'{text}' non è stato trovato.")
        else:
            editor.setTextCursor(found)

def replace_text(editor: QTextEdit):
    """Sostituisce del testo nel documento."""
    find, ok1 = QInputDialog.getText(editor, "Trova", "Testo da trovare:")
    if not ok1 or not find:
        return
    replace, ok2 = QInputDialog.getText(editor, "Sostituisci", "Sostituisci con:")
    if not ok2:
        return
    text = editor.toPlainText().replace(find, replace)
    editor.setPlainText(text)

