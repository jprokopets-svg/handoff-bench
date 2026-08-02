import time


class TokenBucket:
    def __init__(self, capacity, refill_rate):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        # capacity and refill_rate can be floats
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        # start full
        self._tokens = float(capacity)
        # last observed time
        self._last = time.monotonic()

    def _now(self, now):
        return time.monotonic() if now is None else float(now)

    def allow(self, tokens=1.0, now=None):
        # tokens param may be int/float
        tokens = float(tokens)
        # tokens > capacity always False
        if tokens > self.capacity:
            return False
        # tokens <= 0 always True and deduct nothing
        if tokens <= 0.0:
            # still update last observed time to account for refill
            if now is not None:
                self._last = float(now)
            else:
                self._last = time.monotonic()
            return True

        t = self._now(now)
        # refill
        delta = t - self._last
        if delta > 0.0 and self.refill_rate > 0.0:
            self._tokens = min(self.capacity, self._tokens + delta * self.refill_rate)
        # update last observed time
        self._last = t
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False
