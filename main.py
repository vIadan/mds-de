from app.sources.simulate import SimulatedMessageSource, SimulatedFileSource
from app.worker.pool import ThreadPoolWorkerPool
from app.processors.batch_collector import MinibatchCollector
from app.processors.nightly_processor import NightlyFileProcessor
from app.bucketing.greedy import GreedyBucketingStrategy
import time
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] (%(origin)s) - %(message)s')

def minibatch_stream_processing():
    print('\n')

    source = SimulatedMessageSource(rate_per_min=10)
    pool = ThreadPoolWorkerPool()
    collector = MinibatchCollector(source=source, pool=pool, window_duration=10)

    print('\n---------------------------------\n')

    collector.run()

    time.sleep(60)

def nightly_file_processing():

    source = SimulatedFileSource()
    pool = ThreadPoolWorkerPool()
    strategy = GreedyBucketingStrategy()
    processor = NightlyFileProcessor(file_source=source, bucketing_strategy=strategy, pool=pool)

    processor.run()

if __name__ == "__main__":
    nightly_file_processing()