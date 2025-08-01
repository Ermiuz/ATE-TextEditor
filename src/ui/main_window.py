from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QFont, QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QTabWidget, QToolBar, QFileDialog, QMessageBox, QFontDialog, QMenu
from ui.tab_data import TabData
from ui.highlighter import Highlighter
from ui.theme import apply_theme
from utils.file_formats import open_file, save_file, is_supported_format
from utils.file_format_selector import FileFormatSelector
from core.plugin_loader import load_plugins
import sys
import os
from ui.code_editor import CodeEditor

HIGHLIGHTING_SUPPORTED = [
    '.py', '.java', '.js', '.rb', '.rs', '.php', '.md', '.sh',
    '.c', '.cpp', '.cs', '.html', '.css', '.sql', '.swift', '.go',
    '.kt', '.pl', '.dart', '.ts', '.scala', '.lua', '.hs', '.erl',
    '.r', '.asm', '.vb', '.fs', '.groovy', '.jl', '.nim', '.vhd',
    '.v', '.xml', '.json', '.yaml', '.toml'
]

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Text Editor - by Ermanno")
        self.setWindowIcon(QIcon("../assets/icon.png"))
        self.setGeometry(100, 100, 1000, 700)
        self.file_paths = {}
        self.recent_files = []
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.setup_toolbar()
        self.add_new_tab()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        load_plugins(self)
        
        # Carica ultimo file aperto se esiste
        if self.recent_files:
            self.open_file(self.recent_files[0])
        
        # Controlla se è la prima esecuzione
        self.first_run = not os.path.exists(os.path.expanduser("~/.config/texteditor/settings.json"))
        if self.first_run:
            self.register_as_default_editor()
        
    def register_as_default_editor(self):
        msg = QMessageBox()
        msg.setWindowTitle("Registra come editor predefinito?")
        msg.setText("Vuoi impostare TextEditor come editor predefinito per i file di testo?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            import subprocess
            subprocess.run([sys.executable, "./src/integrations/desktop.py"]) 

    def first_run_setup(self):
        success = desktop_integration.register_file_association(self)  # Passa self come parent window
        
        if success:
            print("Registrazione nel sistema completata!")
        else:
            print("Registrazione fallita - usando funzionalità base")
    

    def setup_toolbar(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        def make_action(icon, tooltip, shortcut, callback):
            action = QAction(QIcon(icon), tooltip, self)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(callback)
            self.toolbar.addAction(action)
            return action

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ICON_PATH = lambda name: os.path.join(BASE_DIR, "..", "assets", name)

        make_action(QIcon(ICON_PATH("new.png")), "Nuovo", "Ctrl+N", self.add_new_tab)
        make_action(QIcon(ICON_PATH("open.png")), "Apri", "Ctrl+O", self.open_file_dialog)
        make_action(QIcon(ICON_PATH("save.png")), "Salva", "Ctrl+S", self.save_current_tab)
        make_action(QIcon(ICON_PATH("font.png")), "Font", None, self.change_font)
        self.toolbar.addSeparator()
        make_action(QIcon(ICON_PATH("undo.png")), "Annulla", "Ctrl+Z", self.undo)
        make_action(QIcon(ICON_PATH("redo.png")), "Ripeti", "Ctrl+Y", self.redo)
        self.toolbar.addSeparator()
        make_action(QIcon(ICON_PATH("cut.png")), "Taglia", "Ctrl+X", self.cut)
        make_action(QIcon(ICON_PATH("copy.png")), "Copia", "Ctrl+C", self.copy)
        make_action(QIcon(ICON_PATH("paste.png")), "Incolla", "Ctrl+V", self.paste)
        self.toolbar.addSeparator()
        make_action(QIcon(ICON_PATH("close.png")), "Chiudi scheda", "Ctrl+W", lambda: self.close_tab(self.tabs.currentIndex()))
        make_action(QIcon(ICON_PATH("save_all.png")), "Salva tutto", "Ctrl+Shift+S", self.save_all)
        make_action(QIcon(ICON_PATH("exit.png")), "Esci", "Ctrl+Q", self.close)
        
        icon = QIcon("../assets/save.png")
        print("Icon is null?", icon.isNull())  # <-- DEVE essere False
        action = QAction(icon, "Salva", self)
    
    def close_tab(self, index):
        """Chiude una scheda dopo aver chiesto se salvare le modifiche"""
        editor = self.tabs.widget(index)
        if editor.document().isModified():
            result = QMessageBox.question(
                self,
                "Modifiche non salvate",
                "Vuoi salvare le modifiche prima di chiudere la scheda?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )
            if result == QMessageBox.StandardButton.Save:
                path, _ = QFileDialog.getSaveFileName(self, "Salva file")
                if not path:
                    return  # annullato
                save_file(path, editor.toPlainText())
                self.tabs.setTabText(index, os.path.basename(path))
            elif result == QMessageBox.StandardButton.Cancel:
                return
        # fuori dall'if: rimuovi la scheda
        self.tabs.removeTab(index)


        
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
    
    def save_all(self):
        """Salva tutte le schede - Versione robusta"""
        failed = []
        for i in range(self.tabs.count()):
            if "*" in self.tabs.tabText(i):  # Solo modificati
                if not self.save_file(i, force_dialog=True):
                    failed.append(self.tabs.tabText(i).replace("*",""))
        
        if failed:
            QMessageBox.warning(self, 
                            "Attenzione", 
                            f"Errore salvataggio file:\n{', '.join(failed)}")
            return False
        return True
    
    def add_new_tab(self, content="", filename="Nuovo documento", file_format=".txt"):
        editor = CodeEditor(file_format)
        editor.setFont(QFont("Consolas", 12))
        if file_format in HIGHLIGHTING_SUPPORTED:
            Highlighter(editor.document(), file_format)
        if content:
            editor.setText(content)
        index = self.tabs.addTab(editor, filename)
        self.tabs.setCurrentIndex(index)
        editor.document().contentsChanged.connect(lambda: self.tab_modified(index))
        editor.textChanged.connect(lambda: self.tab_modified(index))
        
    def tab_modified(self, index):
        current_text = self.tabs.tabText(index)
        if not current_text.endswith("*"):
            self.tabs.setTabText(index, current_text + "*")

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Apri file")
        if path and is_supported_format(path):
            content = open_file(path)
            _, ext = os.path.splitext(path)
            self.add_new_tab(content, os.path.basename(path), ext)
        else:
            QMessageBox.warning(self, "Errore", "Formato file non supportato.")

    def save_current_tab(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            editor = self.tabs.widget(index)
            path, _ = QFileDialog.getSaveFileName(self, "Salva file")
            if path:
                save_file(path, editor.toPlainText())
                self.tabs.setTabText(index, os.path.basename(path))

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            for i in range(self.tabs.count()):
                self.tabs.widget(i).setFont(font)
