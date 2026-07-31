"""
Simple regex pattern matching.

Supports:
  '.' - matches any single character
  '*' - matches zero or more of the preceding character

The match must cover the entire input string.
"""


def is_match(s: str, p: str) -> bool:
    """
    Determine if string `s` matches pattern `p`.

    Rules:
      - '.' matches any single character.
      - '*' matches zero or more occurrences of the preceding element.
      - The entire string must be matched (not just a substring).

    Args:
        s: The input string to test.
        p: The pattern string (may contain '.' and '*').

    Returns:
        True if `s` matches `p`, False otherwise.
    """
    # Use dynamic programming.
    # dp[i][j] = True if s[:i] matches p[:j]
    m, n = len(s), len(p)

    # dp table with one extra row/col for empty string/pattern
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    # Empty string matches empty pattern
    dp[0][0] = True

    # Empty string can match patterns like "a*", "a*b*", ".*", etc.
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            # '*' can eliminate the preceding element (zero occurrences)
            dp[0][j] = dp[0][j - 2] if j >= 2 else False

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            pc = p[j - 1]  # current pattern character

            if pc == '*':
                # '*' must have a preceding character (j >= 2 guaranteed by valid pattern)
                prev_pc = p[j - 2]  # the character before '*'

                # Option 1: use '*' as zero occurrences of prev_pc
                zero_match = dp[i][j - 2]

                # Option 2: use '*' as one-or-more occurrences of prev_pc
                #   requires prev_pc matches s[i-1]
                one_or_more = (
                    dp[i - 1][j]
                    if (prev_pc == '.' or prev_pc == s[i - 1])
                    else False
                )

                dp[i][j] = zero_match or one_or_more

            elif pc == '.' or pc == s[i - 1]:
                # Single character match (literal or '.')
                dp[i][j] = dp[i - 1][j - 1]

            else:
                dp[i][j] = False

    return dp[m][n]
