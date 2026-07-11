import numpy as np
import time
from app.sources.base import MessageSource
from app.models.message import Message
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