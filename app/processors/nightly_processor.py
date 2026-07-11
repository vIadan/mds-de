from app.sources.base import FileSource
from app.bucketing.base import BucketingStrategy
from app.worker.base import WorkerPool
from app.worker.tasks import FileBucketTask

class NightlyFileProcessor:

    def __init__(self, file_source: FileSource, bucketing_strategy: BucketingStrategy, pool: WorkerPool):
        self.file_source = file_source
        self.bucketing_strategy = bucketing_strategy
        self.pool = pool

    def run(self):
        files = self.file_source.get_files()
        buckets = self.bucketing_strategy.bucket(files)
        for bucket in buckets:
            bucket_task = FileBucketTask(bucket)
            self.pool.submit(bucket_task)