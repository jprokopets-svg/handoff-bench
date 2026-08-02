from token_bucket_limiter import *


tb = TokenBucket(5, 1.0); assert tb.allow(1, now=0.0); assert tb.allow(4, now=0.0); assert not tb.allow(1, now=0.0)

tb = TokenBucket(5, 1.0); assert tb.allow(5, now=0.0); assert tb.allow(5, now=5.0); assert tb.allow(5, now=100.0); assert not tb.allow(5, now=100.0)

tb = TokenBucket(5, 1.0); assert tb.allow(5, now=0.0); assert not tb.allow(1, now=0.0); assert tb.allow(1, now=1.0)

tb = TokenBucket(2, 1.0); assert not tb.allow(3, now=0.0); assert tb.allow(2, now=0.0); assert not tb.allow(1, now=0.0)

tb = TokenBucket(1, 1.0); assert tb.allow(0, now=0.0); assert tb.allow(-1, now=0.0); assert tb.allow(1, now=0.0)

tb = TokenBucket(5, 1.0); assert tb.allow(3, now=0.0); assert tb.allow(3, now=1.0); assert not tb.allow(1, now=1.5)

tb = TokenBucket(5, 0.5); assert tb.allow(5, now=0.0); assert tb.allow(1, now=2.0); assert not tb.allow(1, now=2.0)

tb = TokenBucket(3, 2.0); assert tb.allow(3, now=0.0); assert not tb.allow(2, now=0.5); assert tb.allow(2, now=1.0); assert not tb.allow(1, now=1.0)