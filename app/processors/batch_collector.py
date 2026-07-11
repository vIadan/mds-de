import threading
import time
import logging
from app.sources.base import MessageSource
from app.worker.base import WorkerPool
from app.models.message import Minibatch
from app.worker.tasks import MinibatchTask

class MinibatchCollector:

    def __init__(self, source: MessageSource, pool: WorkerPool, window_duration: int = 300):
        self.source = source
        self.pool = pool
        self.window_duration = window_duration
        logging.info(f'Message collector of type {__class__.__name__} successfully initialized. It collects messages from {self.source.__class__.__name__} for {self.window_duration} seconds, creates a batch out of them and sends it to {self.pool.__class__.__name__} for processing', extra={'origin': self.__class__.__name__})

    def _collect(self):
        current_batch = None

        for message in self.source.stream():
            if current_batch is None:
                current_batch = Minibatch()
                window_start = time.time()
                logging.info(f'Batch \x1B[3m{current_batch.id}\x1B[0m initialized. Collecting messages during next {self.window_duration} seconds...', extra={'origin': self.__class__.__name__})

            current_batch.add(message)

            if time.time() - window_start >= self.window_duration:
                logging.info(f'Window closed, batch filled. Submitting batch \x1B[3m{current_batch.id}\x1B[0m to workers for processing...', extra={'origin': self.__class__.__name__})
                self.pool.submit(MinibatchTask(current_batch))
                current_batch = None
                window_start = None

        # stream ended, flush if there is something left
        if current_batch and current_batch.messages:
            logging.info(f'Window closed, batch filled. Submitting batch \x1B[3m{current_batch.id}\x1B[0m to workers for processing...', extra={'origin': self.__class__.__name__})
            self.pool.submit(MinibatchTask(current_batch))

    def run(self):
        thread = threading.Thread(target=self._collect, daemon=True)
        thread.start()