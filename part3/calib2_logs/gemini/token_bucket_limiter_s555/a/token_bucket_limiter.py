
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill_time = time.monotonic()

    def allow(self, tokens=1.0, now=None):
        if tokens <= 0:
            return True
        if tokens > self.capacity:
            return False

        if now is None:
            now = time.monotonic()

        time_passed = now - self.last_refill_time
        self.tokens = min(self.capacity, self.tokens + time_passed * self.refill_rate)

        if self.tokens >= tokens:
            self.tokens -= tokens
            self.last_refill_time = now
            return True
        else:
            return False
