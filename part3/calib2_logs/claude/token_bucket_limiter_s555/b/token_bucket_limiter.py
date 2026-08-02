import time


class TokenBucket:
    """
    A token bucket rate limiter that controls request throughput by managing token consumption.
    Tokens refill over time at a configurable rate.
    """

    def __init__(self, capacity: float, refill_rate: float):
        """
        Initialize a token bucket.

        Args:
            capacity: Maximum number of tokens the bucket can hold
            refill_rate: Number of tokens added per unit time (continuous refill)
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity  # Start FULL
        self.last_refill_time = None

    def allow(self, tokens: float = 1.0, now: float | None = None) -> bool:
        """
        Check if enough tokens are available and consume them if so.

        Args:
            tokens: Number of tokens to consume (default 1.0)
            now: Current time for deterministic testing; if None, uses monotonic clock

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
        refilled_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + refilled_tokens)
        self.last_refill_time = now

        # Handle edge cases
        # tokens <= 0 returns True and deducts nothing
        if tokens <= 0:
            return True

        # tokens > capacity always returns False
        if tokens > self.capacity:
            return False

        # Check if we have enough tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True

        return False
