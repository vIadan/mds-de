from abc import ABC, abstractmethod

class MessageSource(ABC):

    @abstractmethod
    def stream(self):
        pass