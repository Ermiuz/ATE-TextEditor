import os
import sys
import subprocess
from pathlib import Path

def register_file_association():
    if sys.platform != 'linux':
        return False

    try:
        app_path = os.path.abspath(sys.argv[0])
        icon_path = os.path.join(os.path.dirname(app_path), 'icon.png')
        desktop_file = f"""
        [Desktop Entry]
        Name=TextEditor
        Exec={app_path} %f
        Icon={icon_path}
        Terminal=false
        Type=Application
        MimeType=text/plain;
        Categories=Utility;TextEditor;
        """

        desktop_path = Path.home() / '.local' / 'share' / 'applications' / 'texteditor.desktop'
        desktop_path.parent.mkdir(parents=True, exist_ok=True)
        with open(desktop_path, 'w') as f:
            f.write(desktop_file)
        os.chmod(desktop_path, 0o755)
        subprocess.run(['update-desktop-database', str(desktop_path.parent)])
        subprocess.run(['xdg-mime', 'default', 'texteditor.desktop', 'text/plain'])
        return True
    except Exception as e:
        print(f"Errore registrazione: {e}")
        return False
