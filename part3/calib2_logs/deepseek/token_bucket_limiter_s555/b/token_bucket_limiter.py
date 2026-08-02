import time
import threading

class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity  # Start full
        self.last_time = time.monotonic()
        self.lock = threading.Lock()
    
    def allow(self, tokens: float = 1.0, now: float | None = None) -> bool:
        if tokens <= 0:
            return True
        
        if tokens > self.capacity:
            return False
        
        with self.lock:
            current_time = now if now is not None else time.monotonic()
            
            # Calculate time elapsed since last observation, but never negative
            time_elapsed = max(0.0, current_time - self.last_time)
            
            # Refill tokens based on elapsed time
            refill_amount = time_elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + refill_amount)
            
            # Update last observation time
            self.last_time = current_time
            
            # Check if we have enough tokens
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False