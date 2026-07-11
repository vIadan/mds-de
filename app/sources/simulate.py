import numpy as np
import time
from app.sources.base import MessageSource, FileSource
from app.models.message import Message
from app.models.file import File
import logging

class SimulatedMessageSource(MessageSource):

    def __init__(self, rate_per_min: int = 10):
        self.rate_per_min = rate_per_min
        logging.info(f'Message source of type {__class__.__name__} successfully initialized', extra={'origin': self.__class__.__name__})

    def stream(self):
        rate_per_sec = self.rate_per_min / 60
        while True:
            wait_time = np.random.exponential(1 / rate_per_sec)
            time.sleep(wait_time)
            logging.info(f'New message have just been published!', extra={'origin': self.__class__.__name__})
            yield Message(content=f'message at {time.time()}')

class SimulatedFileSource(FileSource):

    def __init__(self, mean_file_size: int = 5):
        self.mean_file_size = mean_file_size

    def get_files(self):
        files = []
        for i in range(1, 101):
            file = File(name=f'file_{i}.csv', size_in_bytes=int(np.random.exponential(scale=self.mean_file_size*1024**2)))
            files.append(file)

        return files