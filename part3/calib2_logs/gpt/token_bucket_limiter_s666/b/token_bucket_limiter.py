from time import monotonic


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        """Create a token bucket with given capacity and refill_rate (tokens per unit time).

        The bucket starts full.
        """
        try:
            capacity = float(capacity)
            refill_rate = float(refill_rate)
        except (TypeError, ValueError):
            raise TypeError("capacity and refill_rate must be numeric")
        if capacity < 0 or refill_rate < 0:
            raise ValueError("capacity and refill_rate must be >= 0")

        self._capacity = capacity
        self._refill = refill_rate
        self._tokens = capacity
        # last observation time (monotonic clock). For deterministic tests, allow() accepts an explicit now.
        self._last = monotonic()

    def allow(self, tokens: float = 1.0, now: float | None = None) -> bool:
        """Attempt to consume `tokens` from the bucket.

        If `now` is provided it is treated as the current time (for deterministic testing).
        Returns True and deducts tokens if enough are available; otherwise returns False and does not deduct.

        tokens > capacity always returns False. tokens <= 0 returns True and deducts nothing.
        """
        # Validate and normalize tokens
        try:
            tokens = float(tokens)
        except (TypeError, ValueError):
            raise TypeError("tokens must be a numeric value")

        # Short-circuit behavior
        if tokens <= 0:
            return True
        if tokens > self._capacity:
            return False

        # Determine current time
        t = now if now is not None else monotonic()
        try:
            t = float(t)
        except (TypeError, ValueError):
            raise TypeError("now must be a numeric timestamp")

        # Compute elapsed time (do not allow negative rewind)
        elapsed = t - self._last
        if elapsed < 0:
            elapsed = 0.0
        # Refill tokens based on elapsed
        if elapsed > 0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._refill)
        # Update last observation to t
        self._last = t

        # Check availability
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False
