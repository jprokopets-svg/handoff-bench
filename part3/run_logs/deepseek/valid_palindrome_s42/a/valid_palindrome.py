def valid_palindrome(s: str) -> bool:
    # Filter alphanumeric characters and convert to lowercase
    filtered = ''.join(ch.lower() for ch in s if ch.isalnum())
    # Check palindrome
    return filtered == filtered[::-1]