to execute having all file listed in the same folder as the main.py:


pyinstaller --name=v1.0-ATE   --onefile   --noconfirm   --windowed   --icon=assets/icon.png   --add-data
 "./assets:assets" --add-data "desktop.py:desktop.py" --add-data "editor_logic.py:editor_logic.py"
 --add-data "file_formats.py:file_formats.py" --add-data "file_format_selector.py:file_format_selector.py"
 --add-data "highlighter.py:highlighter.py" --add-data "main_window.py:main_window.py"
 --add-data "plugin_loader.py:plugin_loader.py" --add-data "settings.py:settings.py"
 --add-data "tab_data.py:tab_data.py" --add-data "theme.py:theme.py"   main.py
