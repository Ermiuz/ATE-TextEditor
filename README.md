--- This is an Advanced Text Editor v1.0 made by Ermanno Incontri © (with all rights reserved). It's Open-source and completely free and customizable, but not to make your own property!

## 🔌 Custom Plugins
ATE® supports **custom Python plugins**.

-------------------------------------

### 📁 Where to put them
Put your plugins into the dir: "./plugins"

-------------------------------------

### How to write a plugin and make it work
Every file `.py` in the dir `plugins/` will be load automatically if it contains at least a function called `init`.
This function receives in input the widget from the editor (`QTextEdit`), thus you can modify or add functionalities and modifications.
Just after the modification, run on the venv in terminal (which you can activate with "source venv/bin/activate - for linux & Mac" or "venv\Scripts\activate - for Windows") the following command **"pyinstaller --onefile --windowed --name "*" --add-data "../plugins/*;plugins" --add-binary "$(python -c 'import PyQt6.Qt6 as qt; print(qt.__file__)')/Qt6/plugins/*;PyQt6/Qt6/plugins" main.py "** -> ("": the name is not necessary) to have the executable file with the custom plugins.

-------------------------------------

### 📦 Example `plugins/spellcheck.py`:

def init(text_edit):
    print("Spellcheck plugin activated.")
    text_edit.setPlaceholderText("Ortogtaphy Corrector Enabled!")
    
Enjoy using ATE®, Bye! ---
