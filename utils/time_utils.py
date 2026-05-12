import time

def get_nanosecond_time() -> int:
    """Returns the current time in nanoseconds since the epoch. Essential for HFT."""
    return time.time_ns()

def get_microsecond_time() -> int:
    """Returns current time in microseconds."""
    return time.time_ns() // 1000

def get_millisecond_time() -> int:
    """Returns current time in milliseconds."""
    return int(time.time() * 1000)

class Timer:
    """A context manager for timing code execution block latency."""
    def __init__(self, name="Timer", logger=None):
        self.name = name
        self.logger = logger
        self.start_ns = 0

    def __enter__(self):
        self.start_ns = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ns = time.time_ns() - self.start_ns
        duration_us = duration_ns / 1000.0
        msg = f"[{self.name}] execution took {duration_us:.3f} microseconds"
        if self.logger:
            self.logger.debug(msg)
        else:
            print(msg)
