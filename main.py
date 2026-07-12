from app.sources.simulate import SimulatedMessageSource, SimulatedFileSource
from app.worker.pool import ThreadPoolWorkerPool
from app.processors.batch_collector import MinibatchCollector
from app.processors.nightly_processor import NightlyFileProcessor
from app.bucketing.greedy import GreedyBucketingStrategy
from bonus.models import Player
from bonus.strategy import RandomSittingStrategy
from bonus.tournament import Tournament
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

def bonus():
    players = [Player(id=i) for i in range(12)]
    strategy = RandomSittingStrategy()
    tournament = Tournament(players=players, num_tables=3, players_per_table=4, strategy=strategy)
    result = tournament.run()

    print(result)

if __name__ == "__main__":
    bonus()