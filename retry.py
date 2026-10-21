"""Retry helper with exponential backoff (demo fixture for a code-review talk)."""

import time


def retry_with_backoff(func, attempts=5, initial_delay=1.0, backoff_factor=2.0, max_delay=30.0):
    """Call func() up to `attempts` times, sleeping between failures."""
    delay = initial_delay
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(delay)
            delay = min(delay * backoff_factor, max_delay)
    raise RuntimeError("unreachable")
