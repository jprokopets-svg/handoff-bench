def full_justify(words, max_width):
    result = []
    current_line = []
    current_length = 0
    i = 0

    while i < len(words):
        word = words[i]
        if not current_line:
            if len(word) <= max_width:
                current_line.append(word)
                current_length = len(word)
                i += 1
            else:
                # This case should not happen based on problem description (word shorter than max_width)
                pass
        elif current_length + 1 + len(word) <= max_width:
            current_line.append(word)
            current_length += 1 + len(word)
            i += 1
        else:
            result.append(format_line(current_line, max_width, False))
            current_line = []
            current_length = 0

    if current_line:
        result.append(format_line(current_line, max_width, True))

    return result

def format_line(words, max_width, is_last_line):
    if is_last_line or len(words) == 1:
        return " ".join(words).ljust(max_width)

    total_word_length = sum(len(word) for word in words)
    total_spaces = max_width - total_word_length
    num_gaps = len(words) - 1

    if num_gaps == 0:  # Should only happen if len(words) == 1, handled above
        return words[0].ljust(max_width)

    space_per_gap = total_spaces // num_gaps
    extra_spaces = total_spaces % num_gaps

    justified_line = words[0]
    for j in range(1, len(words)):
        num_spaces = space_per_gap
        if extra_spaces > 0:
            num_spaces += 1
            extra_spaces -= 1
        justified_line += " " * num_spaces + words[j]
    return justified_line
