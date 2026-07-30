def longest_common_prefix(strs: list[str]) -> str:
    # Handle empty list
    if not strs:
        return ''
    
    # Handle single string
    if len(strs) == 1:
        return strs[0]
    
    # Find the minimum length among all strings
    min_len = min(len(s) for s in strs)
    
    # Compare characters at each position
    for i in range(min_len):
        char = strs[0][i]
        # Check if all strings have the same character at position i
        for j in range(1, len(strs)):
            if strs[j][i] != char:
                # Mismatch found, return prefix up to this point
                return strs[0][:i]
    
    # All characters matched up to min_len
    return strs[0][:min_len]
