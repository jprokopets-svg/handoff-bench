def full_justify(words: list[str], max_width: int) -> list[str]:
    """Fully justify the given words into lines of width max_width.

    Greedy: pack as many words as possible on each line. For non-last lines,
    distribute spaces evenly between words, giving the leftmost gaps the extra
    spaces when necessary. The last line is left-justified (single spaces
    between words and trailing spaces to fill width). A line with a single
    word is left-justified (padded with trailing spaces).
    """
    if max_width <= 0:
        raise ValueError("max_width must be positive")

    res: list[str] = []
    n = len(words)
    i = 0
    while i < n:
        # determine which words fit on this line
        j = i
        line_len = 0  # sum of word lengths in this line
        while j < n:
            word_len = len(words[j])
            if line_len + word_len + (j - i) > max_width:
                break
            line_len += word_len
            j += 1
        # words from i to j-1 go on this line
        num_words = j - i
        is_last = (j == n)
        if num_words == 1 or is_last:
            # left-justified: words separated by single spaces, pad end
            line = " ".join(words[i:j])
            line += " " * (max_width - len(line))
            res.append(line)
        else:
            # fully justify: distribute spaces among gaps
            total_spaces = max_width - line_len
            gaps = num_words - 1
            base_space = total_spaces // gaps
            extra = total_spaces % gaps
            parts = []
            for k in range(num_words):
                parts.append(words[i + k])
                if k < gaps:
                    # for the first `extra` gaps add one more space
                    space_count = base_space + (1 if k < extra else 0)
                    parts.append(" " * space_count)
            line = "".join(parts)
            res.append(line)
        i = j
    return res
