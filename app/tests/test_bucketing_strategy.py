from app.models.file import File
from app.bucketing.greedy import GreedyBucketingStrategy
from app.sources.simulate import SimulatedFileSource

def test_greedy_bucketing_strategy_bucket_size():
    files = []
    for i in range(9):
        files.append(File(name=f'file_{i}', size_in_bytes=3 * 1024 ** 2)) # 9 files x 3MB = 27MB, expecting 3 buckets with 3 x 3MB files inside

    total_num_files_input = len(files)

    strategy = GreedyBucketingStrategy()
    buckets = strategy.bucket(files)

    assert len(buckets) == 3

    total_num_files_output = 0
    for bucket in buckets:
        total_num_files_output += len(bucket.files)

        assert len(bucket.files) == 3
        assert bucket.total_size == 9 * 1024**2
        
    assert total_num_files_output == total_num_files_input

def test_simulated_file_source_get_files():
    source = SimulatedFileSource()
    files = source.get_files()

    assert len(files) == 100
    assert all(isinstance(file, File) for file in files)