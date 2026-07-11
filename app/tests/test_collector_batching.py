from app.sources.base import MessageSource
from app.processors.batch_collector import MinibatchCollector
from app.worker.base import WorkerPool, Task
from app.models.message import Message
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

def test_collector_creates_multiple_batches():
    messages = [Message('m1'), Message('m2'), Message('m3'), Message('m4'), Message('m6'), Message('m6')]
    source = MockMessageSource(messages=messages, delay=0.5)
    pool = MockWorkerPool()
    collector = MinibatchCollector(source=source, pool=pool, window_duration=1)

    collector.run()
    time.sleep(4)

    assert len(pool.submitted) == 2
    assert len(pool.submitted[0].batch.messages) == 3
    assert len(pool.submitted[1].batch.messages) == 3

def test_collector_on_empty_stream():
    messages = []
    source = MockMessageSource(messages)
    pool = MockWorkerPool()
    collector = MinibatchCollector(source=source, pool=pool, window_duration=1)

    collector.run()

    assert len(pool.submitted) == 0