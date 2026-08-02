def full_justify(words: list[str], max_width: int) -> list[str]:
    """
    Format words into fully-justified lines of exactly max_width characters.
    
    Greedy packing: add words to current line while they fit.
    Non-last lines: fully justified with spaces distributed left-to-right for extras.
    Last line: left-justified with single spaces and trailing padding.
    """
    if not words:
        return []
    
    result = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Check if adding this word would exceed max_width
        # current_length is the sum of word lengths, plus we need at least (len(current_line) - 1) spaces
        # if we add a new word, we'd need len(current_line) spaces minimum
        if current_length + len(word) + len(current_line) > max_width:
            # Current line is full, justify it and start a new line
            result.append(justify_line(current_line, max_width, False))
            current_line = []
            current_length = 0
        
        current_line.append(word)
        current_length += len(word)
    
    # Handle the last line (left-justified)
    if current_line:
        result.append(justify_line(current_line, max_width, True))
    
    return result


def justify_line(words: list[str], max_width: int, is_last: bool) -> str:
    """
    Justify a single line of words.
    
    If is_last is True: left-justify with single spaces and trailing padding.
    If is_last is False: fully justify with spaces distributed left-to-right.
    """
    if is_last:
        # Left-justify: single spaces between words, pad with trailing spaces
        line = ' '.join(words)
        return line + ' ' * (max_width - len(line))
    
    # Full justification for non-last lines
    if len(words) == 1:
        # Single word: left-justify with trailing padding
        return words[0] + ' ' * (max_width - len(words[0]))
    
    # Multiple words: distribute spaces
    total_word_length = sum(len(word) for word in words)
    total_spaces = max_width - total_word_length
    gaps = len(words) - 1
    
    spaces_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps
    
    line = ''
    for i, word in enumerate(words[:-1]):
        line += word
        # Add base spaces plus one extra if this gap gets an extra space
        spaces = spaces_per_gap + (1 if i < extra_spaces else 0)
        line += ' ' * spaces
    
    line += words[-1]
    return line
