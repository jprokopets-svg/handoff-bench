def full_justify(words: list[str], max_width: int) -> list[str]:
    """Fully justify a list of words to lines of length max_width.

    If a word is longer than max_width it will be split into chunks of length max_width.
    """
    if max_width <= 0:
        raise ValueError("max_width must be positive")

    # Preprocess: split words longer than max_width into chunks
    proc: list[str] = []
    for w in words:
        if len(w) <= max_width:
            proc.append(w)
        else:
            # split into chunks of at most max_width
            start = 0
            while start < len(w):
                proc.append(w[start:start+max_width])
                start += max_width

    res: list[str] = []
    n = len(proc)
    i = 0
    while i < n:
        j = i
        line_len = 0  # sum of word lengths in the line
        # try to fit as many words as possible: line_len + len(next) + spaces_between <= max_width
        while j < n and line_len + len(proc[j]) + (j - i) <= max_width:
            line_len += len(proc[j])
            j += 1

        num_words = j - i
        # If this is the last line or the line has a single word -> left-justify
        if j == n or num_words == 1:
            line = " ".join(proc[i:j])
            # pad with spaces to the right
            line += " " * (max_width - len(line))
        else:
            total_spaces = max_width - line_len
            gaps = num_words - 1
            space, extra = divmod(total_spaces, gaps)
            parts = []
            for k in range(i, j - 1):
                # for the leftmost 'extra' gaps add one more space
                add = space + (1 if (k - i) < extra else 0)
                parts.append(proc[k] + (" " * add))
            parts.append(proc[j - 1])
            line = "".join(parts)
        res.append(line)
        i = j

    return res
