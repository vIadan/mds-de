import threading
from app.sources.base import FileSource
from app.bucketing.base import BucketingStrategy
from app.worker.base import WorkerPool
from app.worker.tasks import FileBucketTask

class NightlyFileProcessor:

    def __init__(self, file_source: FileSource, bucketing_strategy: BucketingStrategy, pool: WorkerPool):
        self.file_source = file_source
        self.bucketing_strategy = bucketing_strategy
        self.pool = pool

    def _process(self):
        files = self.file_source.get_files()
        buckets = self.bucketing_strategy.bucket(files)
        for bucket in buckets:
            self.pool.submit(FileBucketTask(bucket))

    def run(self):
        thread = threading.Thread(target=self._process, daemon=True)
        thread.start()