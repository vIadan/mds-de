from abc import ABC, abstractmethod

class Task(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

class WorkerPool(ABC):

    @abstractmethod
    def submit(self, task: Task):
        pass