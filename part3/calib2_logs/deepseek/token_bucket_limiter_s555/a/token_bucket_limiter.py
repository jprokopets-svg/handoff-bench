import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_time = None  # Will be set on first call
    
    def allow(self, tokens=1.0, now=None):
        if tokens <= 0:
            return True
        
        if tokens > self.capacity:
            return False
        
        if now is None:
            now = time.monotonic()
        
        # Initialize last_time if this is the first call
        if self.last_time is None:
            self.last_time = now
        
        # Calculate time elapsed since last update
        elapsed = now - self.last_time
        self.last_time = now
        
        # Add tokens based on elapsed time
        self.tokens += elapsed * self.refill_rate
        if self.tokens > self.capacity:
            self.tokens = self.capacity
        
        # Check if we have enough tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False