import os
import importlib.util

def load_plugins(editor_instance):
    plugins_dir = os.path.join(os.path.dirname(__file__), "..", "plugins")
    if not os.path.isdir(plugins_dir):
        return

    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(plugins_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            plugin = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(plugin)
                if hasattr(plugin, "init"):
                    plugin.init(editor_instance)
            except Exception as e:
                print(f"Errore nel plugin {filename}: {e}")
