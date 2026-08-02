
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill_time = 0.0 # Initialize to 0.0 for deterministic testing

    def allow(self, tokens=1.0, now=None):
        if tokens <= 0:
            return True
        if tokens > self.capacity:
            return False

        if now is None:
            current_time = time.monotonic()
        else:
            current_time = now

        time_elapsed = current_time - self.last_refill_time
        self.tokens = min(self.capacity, self.tokens + time_elapsed * self.refill_rate)
        self.last_refill_time = current_time

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False
