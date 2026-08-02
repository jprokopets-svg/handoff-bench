def full_justify(words: list[str], max_width: int) -> list[str]:
    result = []
    i = 0
    n = len(words)
    
    while i < n:
        # Start a new line
        line_words = []
        line_length = 0
        
        # Greedy packing: add words while they fit
        while i < n:
            word = words[i]
            # Check if we can add this word to the current line
            # For the first word, no space before it
            # For subsequent words, need at least one space
            if line_length == 0:
                new_length = len(word)
            else:
                new_length = line_length + 1 + len(word)
            
            if new_length <= max_width:
                line_words.append(word)
                line_length = new_length
                i += 1
            else:
                break
        
        # Format the line
        if i == n:  # Last line
            # Left-justified with single spaces
            line = ' '.join(line_words)
            # Pad with trailing spaces
            line += ' ' * (max_width - len(line))
        else:
            # Not the last line, fully justify
            num_words = len(line_words)
            if num_words == 1:
                # Single word line: left-justified with trailing spaces
                line = line_words[0] + ' ' * (max_width - len(line_words[0]))
            else:
                # Multiple words: distribute spaces
                total_spaces = max_width - sum(len(w) for w in line_words)
                gaps = num_words - 1
                base_spaces = total_spaces // gaps
                extra_spaces = total_spaces % gaps
                
                # Build the line
                parts = []
                for j in range(num_words - 1):
                    parts.append(line_words[j])
                    # Add base spaces
                    spaces_to_add = base_spaces
                    # Add extra space for leftmost gaps
                    if j < extra_spaces:
                        spaces_to_add += 1
                    parts.append(' ' * spaces_to_add)
                
                # Add the last word
                parts.append(line_words[-1])
                line = ''.join(parts)
        
        result.append(line)
    
    return result