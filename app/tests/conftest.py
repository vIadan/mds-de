from app.sources.base import MessageSource
from app.worker.base import WorkerPool, Task
import time

class MockMessageSource(MessageSource):
    def __init__(self, messages, delay=0):
        self.messages = messages
        self.delay = delay

    def stream(self):
        for message in self.messages:
            time.sleep(self.delay)
            yield message

class MockWorkerPool(WorkerPool):
    def __init__(self):
        self.submitted = []

    def submit(self, task: Task):
        self.submitted.append(task)

