from abc import ABC, abstractmethod

class MessageSource(ABC):

    @abstractmethod
    def stream(self):
        pass

class FileSource(ABC):

    @abstractmethod
    def get_files(self):
        pass