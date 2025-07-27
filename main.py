import sys
import json
import PyQt6
from PyQt6 import (QtWidgets, QtGui, QtCore)
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QFileDialog, QTabWidget, QToolBar, QVBoxLayout, QWidget, QMessageBox, QMenu, QFontDialog)
from PyQt6.QtGui import (QPalette, QColor, QFont, QIcon, QTextCharFormat, QSyntaxHighlighter, QTextDocument, QAction, QTextOption)
from PyQt6.QtCore import Qt, QRegularExpression
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        ...
        self.load_plugins()  # <-- questa riga è OK

    def load_plugins(self):  # <-- deve stare DENTRO la classe
        import os, importlib.util
        print("Plugin loader chiamato!")

        plugins_dir = os.path.join(os.path.dirname(__file__), "..", "plugins")
        for filename in os.listdir(plugins_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(plugins_dir, filename)
                spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
                plugin = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(plugin)
                    if hasattr(plugin, "init"):
                        plugin.init(self.text_edit)  # o altro oggetto
                except Exception as e:
                    print(f"Errore nel caricamento del plugin {filename}: {e}")

class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlight_rules = []
        
        # Formato per le parole chiave
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(0, 0, 255))  # Blu
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = ["def", "class", "return", "import", "from", "as"]
        self.highlight_rules.extend(
            (r'\b%s\b' % keyword, keyword_format) for keyword in keywords
        )

    def highlightBlock(self, text):
        for pattern, fmt in self.highlight_rules:
            expression = QRegularExpression(pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class TextEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Text Editor - by Ermanno")
        self.setWindowIcon(QIcon("../assets/advanced_text_editor_logo.ico"))
        self.setWindowIcon(QIcon("../assets/advanced_text_editor_logo_clean.png"))
        self.setGeometry(100, 100, 1000, 700)
        
        # Configurazione impostazioni
        self.settings = QtCore.QSettings("MyCompany", "TextEditor")
        self.recent_files = self.settings.value("recentFiles", [])
        
        # Variabili di stato
        self.current_theme = self.settings.value("theme", "light")
        self.font_family = self.settings.value("fontFamily", "Consolas")
        self.font_size = int(self.settings.value("fontSize", 12))
        
        # Setup UI
        self.setup_ui()
        self.apply_theme(self.current_theme)
        self.apply_font(QFont(self.font_family, self.font_size))
        
        # Carica ultimo file aperto se esiste
        if self.recent_files:
            self.open_file(self.recent_files[0])

    def setup_ui(self):
        # Widget centrale con schede
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        
        # Barra degli strumenti
        self.setup_toolbar()
        
        # Menu
        self.setup_menus()
        
        # Aggiungi prima scheda vuota
        self.add_new_tab()
        
        # Applica impostazioni tema e font
        self.apply_theme(self.current_theme)
        self.apply_font(QFont(self.font_family, self.font_size))

    def setup_toolbar(self):
        toolbar = QtWidgets.QToolBar()
        self.addToolBar(toolbar)
        
        # Azioni toolbar
        new_action = QAction(QIcon.fromTheme("document-new"), "Nuovo", self)
        new_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_action)
        
        open_action = QAction(QIcon.fromTheme("document-open"), "Apri", self)
        open_action.triggered.connect(self.open_file_dialog)
        toolbar.addAction(open_action)
        
        save_action = QAction(QIcon.fromTheme("document-save"), "Salva", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        font_action = QAction(QIcon.fromTheme("preferences-desktop-font"), "Font", self)
        font_action.triggered.connect(self.change_font)
        toolbar.addAction(font_action)

    def setup_menus(self):
        menubar = self.menuBar()
        
        # Menu File
        file_menu = menubar.addMenu("File")
        
        # Crea azioni per il menu File
        new_action = QAction("Nuovo", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_action)

        open_action = QAction("Apri...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        save_action = QAction("Salva", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Salva con nome...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        self.recent_menu = file_menu.addMenu("File recenti")
        self.update_recent_files_menu()
        
        file_menu.addSeparator()
        
        exit_action = QAction("Esci", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Modifica
        edit_menu = menubar.addMenu("Modifica")
        
        undo_action = QAction("Annulla", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Ripeti", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Taglia", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copia", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Incolla", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)

        # Menu Visualizza
        view_menu = menubar.addMenu("Visualizza")
        theme_menu = view_menu.addMenu("Temi")
        
        themes = [
            ("Chiaro", "light", "Ctrl+L"),
            ("Scuro", "dark", "Ctrl+D"),
            ("Viola", "purple", "Ctrl+P"),
            ("Vanilla", "vanilla", "Ctrl+I"),
            ("Blu Oceano", "blue", "Ctrl+B")
        ]
        
        for name, theme_id, shortcut in themes:
            action = QtGui.QAction(name, self)
            action.setShortcut(QtGui.QKeySequence(shortcut))
            action.triggered.connect(lambda _, t=theme_id: self.apply_theme(t))
            theme_menu.addAction(action)
        
        view_menu.addSeparator()
        
        zoom_in = QAction("Zoom +", self)
        zoom_in.setShortcut("Ctrl++")
        zoom_in.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in)

        zoom_out = QAction("Zoom -", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out)

        reset_zoom = QAction("Reimposta zoom", self)
        reset_zoom.setShortcut("Ctrl+0")
        reset_zoom.triggered.connect(self.reset_zoom)
        view_menu.addAction(reset_zoom)


    def add_new_tab(self, content="", filename="Nuovo documento"):
        editor = QTextEdit()
        editor.setFont(QFont(self.font_family, self.font_size))
        editor.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        
        # Imposta highlighter
        self.highlighter = Highlighter(editor.document())
        
        if content:
            editor.setText(content)
        
        # Abilita undo/redo
        editor.setUndoRedoEnabled(True)
        
        tab_index = self.tabs.addTab(editor, filename)
        self.tabs.setCurrentIndex(tab_index)
        
        # Collegamento al modifiche per segnare tab come modificato
        editor.document().contentsChanged.connect(lambda: self.tab_modified(tab_index))
        
        return editor

    def tab_modified(self, index):
        current_text = self.tabs.tabText(index)
        if not current_text.endswith("*"):
            self.tabs.setTabText(index, current_text + "*")

    def close_tab(self, index):
        if self.tabs.count() <= 1:
            # Se è l'ultima scheda, aggiungine una nuova prima di chiuderla
            self.add_new_tab()
        
        self.tabs.removeTab(index)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Apri file", "", 
        "Testo (*.txt);;Python (*.py);;Tutti i file (*)")
        if file_path:
            self.open_file(file_path)

    def open_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Controlla se il file è già aperto in un'altra scheda
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == QFileInfo(file_path).fileName():
                    self.tabs.setCurrentIndex(i)
                    return
                    
            # Aggiungi come nuova scheda
            editor = self.add_new_tab(content, QFileInfo(file_path).fileName())
            
            # Aggiorna lista file recenti
            self.update_recent_files(file_path)
            
            return editor
        
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Impossibile aprire il file:\n{str(e)}")
            return None

    def save_file(self):
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
            
        current_index = self.tabs.currentIndex()
        tab_text = self.tabs.tabText(current_index)
        
        # Se è una nuova scheda senza nome file, chiedi dove salvarlo
        if "Nuovo documento" in tab_text or "*" in tab_text:
            return self.save_file_as()
            
        file_path = self.settings.value(f"tab_{current_index}_path", "")
        
        try:
            with open(file_path, 'w') as f:
                f.write(current_editor.toPlainText())
                
            # Rimuovi asterisco modificato
            self.tabs.setTabText(current_index, tab_text.replace("*", ""))
            self.update_recent_files(file_path)
            
            return True
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Impossibile salvare il file:\n{str(e)}")
            return False

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salva file", "", 
        "Testo (*.txt);;Python (*.py);;Tutti i file (*)")
        if file_path:
            current_editor = self.tabs.currentWidget()
            if current_editor:
                try:
                    with open(file_path, 'w') as f:
                        f.write(current_editor.toPlainText())
                        
                    # Aggiorna nome tab
                    self.tabs.setTabText(self.tabs.currentIndex(), QFileInfo(file_path).fileName())
                    self.update_recent_files(file_path)
                    
                    return True
                except Exception as e:
                    QMessageBox.warning(self, "Errore", f"Impossibile salvare il file:\n{str(e)}")
                    return False
        return False

    def update_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
            
        self.recent_files.insert(0, file_path)
        if len(self.recent_files) > 10:
            self.recent_files = self.recent_files[:10]
            
        self.settings.setValue("recentFiles", self.recent_files)
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.recent_menu.clear()
        
        for i, file_path in enumerate(self.recent_files):
            action = self.recent_menu.addAction(f"{i+1}. {QFileInfo(file_path).fileName()}")
            action.setData(file_path)
            action.triggered.connect(lambda _, f=file_path: self.open_file(f))

    def apply_theme(self, theme_name):
        palette = QPalette()
        
        if theme_name == "dark":
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            
        elif theme_name == "purple":
            palette.setColor(QPalette.ColorRole.Window, QColor(70, 20, 90))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Button, QColor(50, 20, 70))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(50, 0, 70))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
            
        elif theme_name == "vanilla":
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 228, 196))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 248, 240))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
            
        elif theme_name == "blue":
            palette.setColor(QPalette.ColorRole.Window, QColor(30, 50, 100))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(15, 30, 70))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(15, 20, 90))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
            
        else:  # light (default)
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        
        # Applica a tutta l'applicazione
        QtWidgets.QApplication.setPalette(palette)
        self.current_theme = theme_name
        
        # Aggiorna tutte le schede
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            widget.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {palette.base().color().name()};
                    color: {palette.text().color().name()};
                    border: none;
                }}
            """)

    def apply_font(self, font):
        self.font_family = font.family()
        self.font_size = font.pointSize()
        
        self.settings.setValue("fontFamily", self.font_family)
        self.settings.setValue("fontSize", self.font_size)
        
        # Applica il font a tutte le schede
        for i in range(self.tabs.count()):
            self.tabs.widget(i).setFont(font)

    def change_font(self):
        font, ok = QFontDialog.getFont(QFont(self.font_family, self.font_size), self)
        if ok:
            self.apply_font(font)

    def zoom_in(self):
        self.font_size += 1
        self.apply_font(QFont(self.font_family, self.font_size))

    def zoom_out(self):
        if self.font_size > 6:
            self.font_size -= 1
            self.apply_font(QFont(self.font_family, self.font_size))

    def reset_zoom(self):
        self.font_size = 12
        self.apply_font(QFont(self.font_family, self.font_size))

    # Metodi per modifiche testo
    def undo(self):
        if editor := self.tabs.currentWidget():
            editor.undo()

    def redo(self):
        if editor := self.tabs.currentWidget():
            editor.redo()

    def cut(self):
        if editor := self.tabs.currentWidget():
            editor.cut()

    def copy(self):
        if editor := self.tabs.currentWidget():
            editor.copy()

    def paste(self):
        if editor := self.tabs.currentWidget():
            editor.paste()

    def closeEvent(self, event):
        # Salva lo stato dell'applicazione
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        # Controlla modifiche non salvate
        unsaved = False
        for i in range(self.tabs.count()):
            if "*" in self.tabs.tabText(i):
                unsaved = True
                break
                
        if unsaved:
            reply = QMessageBox.question(self, "Modifiche non salvate",
            "Ci sono modifiche non salvate. Vuoi uscire comunque?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
                
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("../assets/advanced_text_editor_logo.ico"))
    app.setWindowIcon(QIcon("../assets/advanced_text_editor_logo_clean.png"))  # icona taskbar
    app.setStyle("Fusion")
    
    # Applica palette di default
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(240, 240, 240))
    app.setPalette(palette)
    
    editor = TextEditor()
    
    # Ripristina geometria finestra
    if editor.settings.value("geometry"):
        editor.restoreGeometry(editor.settings.value("geometry"))
    
    editor.show()
    sys.exit(app.exec())
