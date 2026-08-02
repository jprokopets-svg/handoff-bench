from typing import List

def full_justify(words: List[str], max_width: int) -> List[str]:
    result = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Calculate the length if we add this word to the current line
        # current_length is sum of lengths of words in current_line
        # spaces needed = len(current_line) (spaces between words)
        if current_line:
            # If we have words already, we need at least one space before the new word
            new_length = current_length + 1 + len(word)
        else:
            # First word in line
            new_length = len(word)
        
        if new_length <= max_width:
            # Word fits in current line
            current_line.append(word)
            current_length = new_length
        else:
            # Word doesn't fit, justify current line and start new line
            result.append(justify_line(current_line, max_width, False))
            current_line = [word]
            current_length = len(word)
    
    # Handle the last line
    if current_line:
        result.append(justify_line(current_line, max_width, True))
    
    return result

def justify_line(words: List[str], max_width: int, is_last: bool) -> str:
    if len(words) == 1 or is_last:
        # Single word or last line: left justify
        line = ' '.join(words)
        # Pad with spaces to max_width
        return line + ' ' * (max_width - len(line))
    
    # Not last line and multiple words: fully justify
    total_spaces = max_width - sum(len(word) for word in words)
    num_gaps = len(words) - 1
    
    # Base spaces per gap
    base_spaces = total_spaces // num_gaps
    extra_spaces = total_spaces % num_gaps
    
    line_parts = []
    for i in range(len(words)):
        line_parts.append(words[i])
        if i < len(words) - 1:
            # Add spaces for this gap
            spaces = base_spaces + (1 if i < extra_spaces else 0)
            line_parts.append(' ' * spaces)
    
    return ''.join(line_parts)