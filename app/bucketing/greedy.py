from app.bucketing.base import BucketingStrategy
from app.models.file import FileBucket
import logging

class GreedyBucketingStrategy(BucketingStrategy):

    def bucket(self, files: list) -> list:
        buckets = []
        current_bucket = None
        BUCKET_MAX_SIZE = 10 * 1024**2
        
        for file in files:
            if current_bucket is None:
                current_bucket = FileBucket()
                logging.info(f'Bucket \x1B[3m{current_bucket.id}\x1B[23m created successfully', extra={'origin': self.__class__.__name__})

            # check before adding - a single file larger than BUCKET_MAX_SIZE will exceed the limit by design, it cannot be split
            if current_bucket.total_size + file.size_in_bytes > BUCKET_MAX_SIZE:
                buckets.append(current_bucket)
                current_bucket = FileBucket()
                logging.info(f'Bucket \x1B[3m{current_bucket.id}\x1B[23m created successfully', extra={'origin': self.__class__.__name__})

            current_bucket.add(file)
            logging.info(f'File of size {(file.size_in_bytes / 1024**2):.1f} MB added to bucket \x1B[3m{current_bucket.id}\x1B[23m', extra={'origin': self.__class__.__name__})

        if current_bucket and current_bucket.total_size > 0:
            buckets.append(current_bucket)

        return buckets