from app.sources.base import MessageSource
from app.worker.base import WorkerPool, Task
from app.models.message import Message
from app.processors.batch_collector import MinibatchCollector
import time

class MockMessageSource(MessageSource):

    def __init__(self, messages):
        self.messages = messages

    def stream(self):
        for message in self.messages:
            yield message

class MockWorkerPool(WorkerPool):

    def __init__(self):
        self.submitted = []

    def submit(self, task: Task):
        self.submitted.append(task)

def test_collector_submits():
    messages = [Message('m1'), Message('m2'), Message('m3')]
    source = MockMessageSource(messages)
    pool = MockWorkerPool()
    collector = MinibatchCollector(source=source, pool=pool, window_duration=1)

    collector.run()
    time.sleep(2)

    assert len(pool.submitted) == 1
    assert len(pool.submitted[0].batch.messages) == 3