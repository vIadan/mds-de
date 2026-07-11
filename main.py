from app.sources.simulate import SimulatedMessageSource
from app.worker.pool import ThreadPoolWorkerPool
from app.processors.batch_collector import MinibatchCollector
import time
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] (%(origin)s) - %(message)s')

print('\n')

source = SimulatedMessageSource(rate_per_min=10)
pool = ThreadPoolWorkerPool()
collector = MinibatchCollector(source=source, pool=pool, window_duration=10)

print('\n---------------------------------\n')

collector.run()

time.sleep(60)