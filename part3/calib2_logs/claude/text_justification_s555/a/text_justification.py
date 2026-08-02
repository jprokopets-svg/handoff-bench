def full_justify(words, max_width):
    """
    Format a list of words into fully-justified lines of exactly max_width characters.
    
    - Greedy packing: add words to the current line while they fit
    - Words on a line are separated by at least one space
    - Non-last lines: fully justified with extra spaces distributed left to right
    - Last line: left-justified with single spaces between words, padded with trailing spaces
    - Single word lines: left-justified with trailing padding
    
    Args:
        words: List of words to justify
        max_width: Width of each line
    
    Returns:
        List of justified lines
    """
    result = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Check if adding this word would exceed max_width
        # current_length is the length of words + minimum spaces needed between them
        # If we add a new word, we need at least one space before it
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


def justify_line(words, max_width, is_last):
    """
    Justify a single line of words.
    
    Args:
        words: List of words for this line
        max_width: Width of the line
        is_last: True if this is the last line (left-justify), False otherwise (full justify)
    
    Returns:
        Justified line as a string
    """
    if is_last:
        # Left-justify: single spaces between words, pad with trailing spaces
        line = ' '.join(words)
        return line + ' ' * (max_width - len(line))
    
    # Full justify: distribute spaces between words
    if len(words) == 1:
        # Single word: left-justify with trailing padding
        return words[0] + ' ' * (max_width - len(words[0]))
    
    # Multiple words: distribute spaces
    total_word_length = sum(len(word) for word in words)
    total_spaces = max_width - total_word_length
    gaps = len(words) - 1
    
    # Distribute spaces: base spaces per gap + extra spaces from left to right
    spaces_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps
    
    line = ''
    for i, word in enumerate(words):
        line += word
        if i < len(words) - 1:
            # Add base spaces
            line += ' ' * spaces_per_gap
            # Add extra space if this gap gets one
            if i < extra_spaces:
                line += ' '
    
    return line
