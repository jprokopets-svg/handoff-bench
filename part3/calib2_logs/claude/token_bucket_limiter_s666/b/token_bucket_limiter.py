import time


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        """
        Initialize a token bucket rate limiter.
        
        Args:
            capacity: Maximum number of tokens the bucket can hold
            refill_rate: Number of tokens added per unit time
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity  # Start FULL
        self.last_refill_time = None  # Will be set on first allow() call
    
    def allow(self, tokens: float = 1.0, now: float | None = None) -> bool:
        """
        Check if tokens are available and consume them if so.
        
        Args:
            tokens: Number of tokens to consume (default 1.0)
            now: Current time for deterministic testing (uses monotonic clock if None)
        
        Returns:
            True if tokens were consumed, False otherwise
        """
        # Get current time
        if now is None:
            now = time.monotonic()
        
        # Initialize last_refill_time on first call
        if self.last_refill_time is None:
            self.last_refill_time = now
        
        # Refill tokens based on elapsed time
        elapsed = now - self.last_refill_time
        refilled = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + refilled)
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
        
        return False
