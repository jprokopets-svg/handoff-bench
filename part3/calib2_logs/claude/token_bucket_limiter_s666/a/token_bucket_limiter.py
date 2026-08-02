import time


class TokenBucket:
    def __init__(self, capacity, refill_rate):
        """
        Initialize a token bucket rate limiter.
        
        Args:
            capacity: Maximum number of tokens the bucket can hold
            refill_rate: Number of tokens added per unit time (continuous refill)
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity  # Start FULL
        self.last_refill_time = None
    
    def allow(self, tokens=1.0, now=None):
        """
        Check if we can consume the requested number of tokens.
        
        Args:
            tokens: Number of tokens to consume (default 1.0)
            now: Current time for deterministic testing. If None, use monotonic clock.
        
        Returns:
            True if tokens were consumed, False otherwise
        """
        # Get current time
        if now is None:
            now = time.monotonic()
        
        # Initialize last_refill_time on first call
        if self.last_refill_time is None:
            self.last_refill_time = now
        
        # Refill tokens based on time elapsed
        time_elapsed = now - self.last_refill_time
        tokens_to_add = time_elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now
        
        # Handle edge cases
        if tokens <= 0:
            return True
        
        if tokens > self.capacity:
            return False
        
        # Check if we have enough tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False
