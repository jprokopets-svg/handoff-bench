from typing import List

def full_justify(words: List[str], max_width: int) -> List[str]:
    result = []
    current_line = []
    current_length = 0
    
    i = 0
    while i < len(words):
        word = words[i]
        
        # Calculate length if we add this word to current line
        # Spaces needed: len(current_line) spaces between words
        if current_length == 0:
            # First word in line
            new_length = len(word)
        else:
            # Need at least one space before the new word
            new_length = current_length + 1 + len(word)
        
        if new_length <= max_width:
            # Word fits in current line
            current_line.append(word)
            current_length = new_length
            i += 1
        else:
            # Word doesn't fit, process current line
            if len(current_line) == 1:
                # Single word line: left-justified with trailing spaces
                line = current_line[0] + ' ' * (max_width - len(current_line[0]))
            else:
                # Multiple words: distribute spaces
                total_spaces = max_width - (current_length - (len(current_line) - 1))
                # Remove the spaces we counted between words
                # current_length includes spaces between words (1 each)
                # So character count without spaces is current_length - (len(current_line) - 1)
                
                gaps = len(current_line) - 1
                base_spaces = total_spaces // gaps
                extra_spaces = total_spaces % gaps
                
                line_parts = []
                for j in range(gaps):
                    line_parts.append(current_line[j])
                    # Add base spaces
                    spaces = base_spaces
                    # Add extra space for first extra_spaces gaps
                    if j < extra_spaces:
                        spaces += 1
                    line_parts.append(' ' * spaces)
                
                line_parts.append(current_line[-1])
                line = ''.join(line_parts)
            
            result.append(line)
            current_line = []
            current_length = 0
    
    # Process last line
    if current_line:
        # Last line: left-justified with single spaces
        line = ' '.join(current_line)
        line += ' ' * (max_width - len(line))
        result.append(line)
    
    return result