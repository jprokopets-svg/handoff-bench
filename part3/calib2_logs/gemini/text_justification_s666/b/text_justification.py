def full_justify(words: list[str], max_width: int) -> list[str]:
    result = []
    current_line = []
    current_length = 0

    i = 0
    while i < len(words):
        word = words[i]
        # Check if adding the current word exceeds max_width
        # current_length + len(word) + len(current_line) (for spaces)
        if current_length + len(word) + len(current_line) > max_width:
            # Justify the current line
            num_gaps = len(current_line) - 1
            line = ""
            if num_gaps == 0:  # Single word on the line
                line = current_line[0] + " " * (max_width - current_length)
            else:
                total_spaces = max_width - current_length
                spaces_per_gap = total_spaces // num_gaps
                extra_spaces = total_spaces % num_gaps

                for j in range(len(current_line)):
                    line += current_line[j]
                    if j < num_gaps:
                        line += " " * spaces_per_gap
                        if j < extra_spaces:
                            line += " "
            result.append(line)
            current_line = []
            current_length = 0
        else:
            current_line.append(word)
            current_length += len(word)
            i += 1

    # Handle the last line
    if current_line:
        line = " ".join(current_line)
        line += " " * (max_width - len(line))
        result.append(line)

    return result
