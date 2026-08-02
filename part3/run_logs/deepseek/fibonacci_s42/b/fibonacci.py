def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number, where fib(0) = 0 and fib(1) = 1."""
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python fibonacci.py <n>")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
        result = fibonacci(n)
        print(f"fibonacci({n}) = {result}")
    except ValueError as e:
        if "invalid literal" in str(e) or "must be non-negative" in str(e):
            print(f"Error: {e}")
            sys.exit(1)
        else:
            # Re-raise unexpected ValueErrors
            raise