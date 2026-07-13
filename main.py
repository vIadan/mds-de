from app.sources.simulate import SimulatedMessageSource, SimulatedFileSource
from app.worker.pool import ThreadPoolWorkerPool
from app.processors.batch_collector import MinibatchCollector
from app.processors.nightly_processor import NightlyFileProcessor
from app.bucketing.greedy import GreedyBucketingStrategy
import threading
import logging
from logging_config import ColorFormatter

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter('[%(asctime)s] (%(origin)s) - %(message)s'))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

def minibatch_stream_processing(pool: ThreadPoolWorkerPool):
    source = SimulatedMessageSource(rate_per_min=10)
    collector = MinibatchCollector(source=source, pool=pool, window_duration=300)
    collector.run()

def nightly_file_processing(pool: ThreadPoolWorkerPool):
    source = SimulatedFileSource(mean_file_size=5)
    strategy = GreedyBucketingStrategy()
    processor = NightlyFileProcessor(file_source=source, bucketing_strategy=strategy, pool=pool)
    processor.run()

if __name__ == "__main__":
    pool = ThreadPoolWorkerPool()

    nightly_file_processing(pool)
    minibatch_stream_processing(pool)

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
