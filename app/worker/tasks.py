from app.worker.base import Task
from app.models.message import Minibatch
import logging
import time, random

class MinibatchTask(Task):

    def __init__(self, batch: Minibatch):
        self.batch = batch

    def execute(self):
        logging.info(f'Processing batch \x1B[3m{self.batch.id}\x1B[0m with {len(self.batch.messages)} messages. This might take some time...', extra={'origin': self.__class__.__name__})
        time.sleep(random.randint(3, 15))  # simulates real processing work
        logging.info(f'Processing of batch \x1B[3m{self.batch.id}\x1B[0m just finished!', extra={'origin': self.__class__.__name__})

class FileBucketTask(Task):

    def __init__(self, bucket):
        self.bucket = bucket

    def execute(self):
        size_mb = self.bucket.total_size / (1024**2)
        logging.info(f'Processing bucket \x1B[3m{self.bucket.id}\x1B[0m with {len(self.bucket.files)} files ({size_mb:.1f} MB)', extra={'origin': self.__class__.__name__})