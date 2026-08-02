
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    if n == 1:
        return 1

    memo = {0: 0, 1: 1}

    for i in range(2, n + 1):
        memo[i] = memo[i-1] + memo[i-2]

    return memo[n]
