from typing import List


def full_justify(words: List[str], max_width: int) -> List[str]:
    res = []
    n = len(words)
    i = 0
    while i < n:
        # determine which words fit on this line
        line_len = len(words[i])
        j = i + 1
        while j < n and line_len + 1 + len(words[j]) <= max_width:
            line_len += 1 + len(words[j])
            j += 1
        # words from i to j-1
        num_words = j - i
        line = ''
        # If this is the last line or only one word -> left-justify
        if j == n or num_words == 1:
            # join with single spaces
            line = ' '.join(words[i:j])
            # pad spaces at end
            line += ' ' * (max_width - len(line))
        else:
            # fully justify
            total_chars = sum(len(w) for w in words[i:j])
            total_spaces = max_width - total_chars
            gaps = num_words - 1
            space_per_gap = total_spaces // gaps
            extra = total_spaces % gaps
            parts = []
            for k in range(i, j):
                parts.append(words[k])
                if k < j - 1:
                    # number of spaces after this word
                    sp = space_per_gap + (1 if (k - i) < extra else 0)
                    parts.append(' ' * sp)
            line = ''.join(parts)
        res.append(line)
        i = j
    return res
