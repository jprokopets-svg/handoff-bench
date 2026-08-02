def full_justify(words: list[str], max_width: int) -> list[str]:
    result = []
    i = 0
    n = len(words)
    
    while i < n:
        # Start a new line with the current word
        line_words = []
        line_length = 0
        j = i
        
        # Greedy packing: add words while they fit
        while j < n:
            # Calculate new length if we add this word
            # For the first word, no space before; for others, add 1 space
            new_length = line_length + len(words[j])
            if line_words:
                new_length += 1  # Space before word
            
            if new_length <= max_width:
                line_words.append(words[j])
                line_length = new_length
                j += 1
            else:
                break
        
        # Now we have line_words for this line
        # Check if this is the last line (j == n) or line has only one word
        if j == n or len(line_words) == 1:
            # Left justify: single spaces between words
            line = ' '.join(line_words)
            # Pad with spaces to max_width
            line += ' ' * (max_width - len(line))
            result.append(line)
        else:
            # Full justification for non-last line
            total_spaces = max_width - sum(len(w) for w in line_words)
            gaps = len(line_words) - 1
            
            if gaps == 0:
                # Shouldn't happen since we handled single word case above
                base_spaces = 0
                extra_spaces = 0
            else:
                base_spaces = total_spaces // gaps
                extra_spaces = total_spaces % gaps
            
            # Build the justified line
            line = line_words[0]
            for idx in range(1, len(line_words)):
                # Add spaces: base_spaces + (1 extra if idx <= extra_spaces)
                spaces = base_spaces
                if idx <= extra_spaces:
                    spaces += 1
                line += ' ' * spaces + line_words[idx]
            
            result.append(line)
        
        i = j
    
    return result