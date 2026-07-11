import secrets

class File:

    def __init__(self, name, size_in_bytes):
        self.name = name
        self.size_in_bytes = size_in_bytes

class FileBucket:

    def __init__(self):
        self.id = secrets.token_urlsafe(5)
        self.files = []
        self.total_size = 0
    
    def add(self, file: File):
        self.files.append(file)
        self.total_size += file.size_in_bytes