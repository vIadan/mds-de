from app.sources.base import FileSource
from app.models.file import File, FileBucket
from app.bucketing.base import BucketingStrategy
from app.processors.nightly_processor import NightlyFileProcessor
from app.tests.conftest import MockWorkerPool
import time


class MockFileSource(FileSource):

    def get_files(self):
        files = []
        for i in range(3):
            files.append(File(name=f'file_{i}', size_in_bytes=3*1024**2))
        return files


class MockBucketingStrategy(BucketingStrategy):

    def bucket(self, files: list) -> list:
        buckets = []
        for file in files:
            bucket = FileBucket()
            bucket.add(file)
            buckets.append(bucket)
        return buckets

def test_nightly_processor_submits():
    source = MockFileSource()
    strategy = MockBucketingStrategy()
    pool = MockWorkerPool()

    processor = NightlyFileProcessor(file_source=source, bucketing_strategy=strategy, pool=pool)

    processor.run()
    time.sleep(1)  # wait for background thread to finish

    assert len(pool.submitted) == 3