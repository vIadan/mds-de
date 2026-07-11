from abc import ABC, abstractmethod

class BucketingStrategy(ABC):

    @abstractmethod
    def bucket(self, files: list) -> list:
        pass