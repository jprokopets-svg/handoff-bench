def full_justify(words: list[str], max_width: int) -> list[str]:
    result = []
    current_line = []
    current_length = 0

    for word in words:
        # Check if adding the word to the current line exceeds max_width
        # current_length + len(word) + (1 if current_line else 0)
        # The (1 if current_line else 0) accounts for the space needed before the new word
        if current_length + len(word) + len(current_line) > max_width:
            result.append(format_line(current_line, current_length, max_width, False))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)

    if current_line:
        result.append(format_line(current_line, current_length, max_width, True))

    return result

def format_line(words: list[str], current_length: int, max_width: int, is_last_line: bool) -> str:
    num_words = len(words)
    
    if is_last_line or num_words == 1:
        return " ".join(words).ljust(max_width)

    total_spaces_needed = max_width - current_length
    num_gaps = num_words - 1

    spaces_per_gap = total_spaces_needed // num_gaps
    extra_spaces = total_spaces_needed % num_gaps

    justified_line = ""
    for i in range(num_words):
        justified_line += words[i]
        if i < num_gaps:
            justified_line += " " * spaces_per_gap
            if i < extra_spaces:
                justified_line += " "
    return justified_line
