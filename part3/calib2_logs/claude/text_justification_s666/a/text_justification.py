def full_justify(words, max_width):
    """
    Format a list of words into fully-justified lines of exactly max_width characters.
    
    Args:
        words: List of words to justify
        max_width: Maximum width of each line
    
    Returns:
        List of justified lines
    """
    result = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Check if adding this word would exceed max_width
        # current_length is the sum of word lengths, plus we need at least one space between words
        if current_length + len(word) + len(current_line) > max_width:
            # Justify the current line and add it to result
            result.append(justify_line(current_line, max_width, False))
            current_line = []
            current_length = 0
        
        current_line.append(word)
        current_length += len(word)
    
    # Handle the last line (left-justified)
    if current_line:
        result.append(justify_line(current_line, max_width, True))
    
    return result


def justify_line(words, max_width, is_last):
    """
    Justify a single line of words.
    
    Args:
        words: List of words for this line
        max_width: Maximum width of the line
        is_last: Whether this is the last line (left-justified) or not (fully justified)
    
    Returns:
        Justified line string of exactly max_width characters
    """
    if is_last:
        # Last line: left-justified with single spaces between words
        line = ' '.join(words)
        # Pad with trailing spaces
        line += ' ' * (max_width - len(line))
        return line
    
    # Non-last line: fully justified
    if len(words) == 1:
        # Single word on the line: left-justified with trailing padding
        line = words[0]
        line += ' ' * (max_width - len(line))
        return line
    
    # Multiple words: distribute spaces
    total_word_length = sum(len(word) for word in words)
    total_spaces = max_width - total_word_length
    gaps = len(words) - 1
    
    spaces_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps
    
    line = ""
    for i, word in enumerate(words):
        line += word
        if i < len(words) - 1:
            # Add spaces after this word
            spaces = spaces_per_gap
            if i < extra_spaces:
                spaces += 1
            line += ' ' * spaces
    
    return line
