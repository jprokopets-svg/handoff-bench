import time

class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = None # Initialize to None

    def allow(self, tokens: float = 1.0, now: float | None = None) -> bool:
        if tokens <= 0:
            return True
        if tokens > self.capacity:
            return False

        if now is None:
            now = time.monotonic()

        if self.last_refill_time is None: # First call to allow
            self.last_refill_time = now
        
        time_passed = now - self.last_refill_time
        self.last_refill_time = now
        self.tokens = min(self.capacity, self.tokens + time_passed * self.refill_rate)

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False
