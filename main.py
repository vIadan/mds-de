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
from app.logging_config import ColorFormatter

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter('[%(asctime)s] (%(origin)s) - %(message)s'))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

def minibatch_stream_processing(pool: ThreadPoolWorkerPool):
    source = SimulatedMessageSource(rate_per_min=10)
    collector = MinibatchCollector(source=source, pool=pool, window_duration=10)
    collector.run()
    time.sleep(60)

def nightly_file_processing(pool: ThreadPoolWorkerPool):
    source = SimulatedFileSource(mean_file_size=5)
    strategy = GreedyBucketingStrategy()
    processor = NightlyFileProcessor(file_source=source, bucketing_strategy=strategy, pool=pool)
    processor.run()

def tournament_organization_bonus():
    players = [Player(id=i) for i in range(12)]
    strategy = RandomSittingStrategy()
    tournament = Tournament(players=players, num_tables=3, players_per_table=4, strategy=strategy)
    result = tournament.run()
    logging.info(f'Tournament finished. {result}', extra={'origin': 'Tournament'})

if __name__ == "__main__":
    pool = ThreadPoolWorkerPool()

    nightly_file_processing(pool)
    minibatch_stream_processing(pool)

    tournament_organization_bonus()