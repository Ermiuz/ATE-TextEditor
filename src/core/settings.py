from PyQt6.QtCore import QSettings

class EditorSettings:
    def __init__(self, organization='MyCompany', app_name='TextEditor'):
        self.settings = QSettings(organization, app_name)

    def set_value(self, key, value):
        self.settings.setValue(key, value)

    def get_value(self, key, default=None):
        return self.settings.value(key, default)

    def remove_value(self, key):
        self.settings.remove(key)

    def clear_all(self):
        self.settings.clear()

