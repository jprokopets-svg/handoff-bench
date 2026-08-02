import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        """
        Initialize a token bucket rate limiter.
        
        Args:
            capacity: Maximum number of tokens the bucket can hold.
            refill_rate: Number of tokens added per unit time (continuous refill).
        """
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = self.capacity  # Start full
        self.last_update = None  # Will be set on first call to allow
    
    def _refill(self, now):
        """Refill the bucket based on elapsed time."""
        if self.last_update is None:
            # First call: no elapsed time
            self.last_update = now
            return
        
        elapsed = now - self.last_update
        if elapsed > 0:
            self.tokens += elapsed * self.refill_rate
            if self.tokens > self.capacity:
                self.tokens = self.capacity
        self.last_update = now
    
    def allow(self, tokens=1.0, now=None):
        """
        Check if tokens can be consumed.
        
        Args:
            tokens: Number of tokens to consume (default 1.0).
            now: Current time for deterministic testing. If None, uses monotonic clock.
        
        Returns:
            True if tokens were consumed, False otherwise.
        """
        if now is None:
            now = time.monotonic()
        
        # Refill based on current time
        self._refill(now)
        
        # Handle edge cases
        if tokens <= 0:
            return True  # No consumption needed
        if tokens > self.capacity:
            return False  # Can never satisfy
        
        # Check if we have enough tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False