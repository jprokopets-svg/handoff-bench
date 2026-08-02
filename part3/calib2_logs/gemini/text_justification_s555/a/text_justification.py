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
                # This case should not happen based on problem description
                pass
        elif current_length + 1 + len(word) <= max_width:
            current_line.append(word)
            current_length += 1 + len(word)
            i += 1
        else:
            result.append(format_line(current_line, current_length, max_width, False))
            current_line = []
            current_length = 0

    if current_line:
        result.append(format_line(current_line, current_length, max_width, True))

    return result

def format_line(words, current_length, max_width, is_last_line):
    if is_last_line or len(words) == 1:
        return " ".join(words).ljust(max_width)

    num_gaps = len(words) - 1
    total_spaces_needed = max_width - (current_length - num_gaps)

    if num_gaps == 0:
        return words[0].ljust(max_width)

    spaces_per_gap = total_spaces_needed // num_gaps
    extra_spaces = total_spaces_needed % num_gaps

    justified_line = []
    for j in range(len(words)):
        justified_line.append(words[j])
        if j < num_gaps:
            justified_line.append(" " * spaces_per_gap)
            if extra_spaces > 0:
                justified_line.append(" ")
                extra_spaces -= 1
    return "".join(justified_line)
