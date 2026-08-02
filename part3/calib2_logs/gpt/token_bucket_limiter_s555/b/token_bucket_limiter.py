import time


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        """Create a token bucket.

        capacity: maximum tokens the bucket can hold (float >= 0)
        refill_rate: tokens added per unit time (float >= 0)
        The bucket starts full.
        """
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        if refill_rate < 0:
            raise ValueError("refill_rate must be non-negative")
        self._capacity = float(capacity)
        self._refill_rate = float(refill_rate)
        self._tokens = float(capacity)
        # last observed time (monotonic by default).
        self._last = time.monotonic()
        # track whether we've switched to external (test) time
        self._use_external_time = False

    def _now(self, now: float | None) -> float:
        return time.monotonic() if now is None else float(now)

    def allow(self, tokens: float = 1.0, now: float | None = None) -> bool:
        """Attempt to consume `tokens` from the bucket.

        tokens > capacity => always False
        tokens <= 0 => True (no deduction)
        If enough tokens are available (after refill), deduct and return True,
        otherwise return False and deduct nothing.
        """
        # Fast-path for requests that don't consume anything
        if tokens <= 0:
            return True

        # If requesting more than capacity, always reject
        if tokens > self._capacity:
            return False

        # If caller supplies an external now for deterministic behavior,
        # and this is the first time we've seen an external timeline,
        # adopt that timeline's last-observed time so small now values like 0.0
        # work in tests.
        if now is not None and not self._use_external_time:
            self._last = float(now)
            self._use_external_time = True

        t = self._now(now)
        # Prevent backward time moves from increasing tokens artificially
        if t < self._last:
            t = self._last

        # Refill based on elapsed time
        elapsed = t - self._last
        if elapsed > 0 and self._refill_rate > 0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._refill_rate)
        # advance last observed time even if no refill
        self._last = t

        if self._tokens + 1e-12 >= tokens:
            self._tokens -= tokens
            return True
        return False
