from app.tests.conftest import MockMessageSource, MockWorkerPool
from app.models.message import Message
from app.processors.batch_collector import MinibatchCollector
import time


def test_collector_submits_batch_after_window():
    messages = [Message('m1'), Message('m2'), Message('m3')]
    source = MockMessageSource(messages)
    pool = MockWorkerPool()
    collector = MinibatchCollector(source=source, pool=pool, window_duration=1)

    collector.run()
    time.sleep(2)

    assert len(pool.submitted) == 1
    assert len(pool.submitted[0].batch.messages) == 3


def test_collector_creates_multiple_batches():
    messages = [Message('m1'), Message('m2'), Message('m3'), Message('m4'), Message('m5'), Message('m6')]
    source = MockMessageSource(messages=messages, delay=0.5)
    pool = MockWorkerPool()
    collector = MinibatchCollector(source=source, pool=pool, window_duration=1)

    collector.run()
    time.sleep(4)  # wait for background thread to finish processing all messages (6 x 0.5s delay)

    assert len(pool.submitted) == 2
    assert len(pool.submitted[0].batch.messages) == 3
    assert len(pool.submitted[1].batch.messages) == 3


def test_collector_on_empty_stream():
    source = MockMessageSource(messages=[])
    pool = MockWorkerPool()
    collector = MinibatchCollector(source=source, pool=pool, window_duration=1)

    collector.run()

    assert len(pool.submitted) == 0
