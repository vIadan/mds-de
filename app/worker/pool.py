from app.worker.base import WorkerPool, Task
from concurrent.futures import ThreadPoolExecutor
import logging

class ThreadPoolWorkerPool(WorkerPool):

    def __init__(self, num_workers: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        logging.info(f'Worker pool of type {__class__.__name__} with {num_workers} successfully initialized', extra={'origin': self.__class__.__name__})

    def submit(self, task: Task) -> None:
        self.executor.submit(task.execute)