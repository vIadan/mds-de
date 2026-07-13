import logging

COLORS = {
    'yellow': '\033[33m',
    'cyan': '\033[36m',
    'green': '\033[32m',
    'magenta': '\033[35m',
    'reset': '\033[0m'
}

ORIGIN_COLORS = {
    'MinibatchCollector': COLORS['yellow'],
    'SimulatedMessageSource': COLORS['yellow'],
    'MinibatchTask': COLORS['yellow'],
    'GreedyBucketingStrategy': COLORS['cyan'],
    'FileBucketTask': COLORS['cyan'],
    'NightlyFileProcessor': COLORS['cyan'],
    'ThreadPoolWorkerPool': COLORS['green'],
    'Tournament': COLORS['magenta'],
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = ORIGIN_COLORS.get(getattr(record, 'origin', ''), '')
        formatted = super().format(record)
        return f"{color}{formatted}{COLORS['reset']}"
