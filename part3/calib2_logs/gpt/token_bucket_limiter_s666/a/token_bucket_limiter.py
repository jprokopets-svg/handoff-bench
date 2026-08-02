import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        if refill_rate < 0:
            raise ValueError("refill_rate must be non-negative")
        self._capacity = float(capacity)
        self._refill_rate = float(refill_rate)
        self._tokens = float(capacity)  # start full
        # last observation time; None until first allow() call
        self._last_time = None

    def allow(self, tokens=1.0, now=None):
        # convert tokens to float if possible
        try:
            tokens = float(tokens)
        except Exception:
            tokens = tokens

        # tokens > capacity always False
        if tokens > self._capacity:
            return False
        # tokens <= 0 returns True and deducts nothing
        if tokens <= 0.0:
            return True

        current_time = now if now is not None else time.monotonic()
        current_time = float(current_time)

        if self._last_time is None:
            # first observation; set baseline
            self._last_time = current_time
            elapsed = 0.0
        else:
            elapsed = current_time - self._last_time

        if elapsed > 0.0:
            # refill continuously but never above capacity
            self._tokens = min(self._capacity, self._tokens + elapsed * self._refill_rate)

        # update last observation time to current (even if elapsed <= 0)
        self._last_time = current_time

        # allow if enough tokens
        if self._tokens + 1e-12 >= tokens:
            self._tokens -= tokens
            return True
        return False

__all__ = ["TokenBucket"]
