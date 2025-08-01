import os

def get_supported_formats():
    return {
        '.txt': 'text/plain',
        '.py': 'text/x-python',
        '.java': 'text/x-java',
        '.js': 'application/javascript',
        '.html': 'text/html',
        '.css': 'text/css',
        '.json': 'application/json',
        '.md': 'text/markdown',
    }

def is_supported_format(file_path):
    _, ext = os.path.splitext(file_path)
    return ext in get_supported_formats()

def open_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
