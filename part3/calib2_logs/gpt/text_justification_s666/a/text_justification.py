from typing import List


def full_justify(words: List[str], max_width: int) -> List[str]:
    res: List[str] = []
    n = len(words)
    i = 0
    while i < n:
        # determine how many words fit on this line
        j = i
        line_len = 0  # sum of lengths of words in this line
        while j < n:
            if line_len + len(words[j]) + (j - i) <= max_width:
                line_len += len(words[j])
                j += 1
            else:
                break
        # words from i to j-1
        num_words = j - i
        line = ""
        # if last line or single word in line -> left-justify
        if j == n or num_words == 1:
            # join with single spaces
            line = ' '.join(words[i:j])
            # pad with spaces
            line += ' ' * (max_width - len(line))
        else:
            total_spaces = max_width - line_len
            gaps = num_words - 1
            base_spaces = total_spaces // gaps
            extra = total_spaces % gaps
            parts = []
            for k in range(gaps):
                parts.append(words[i + k])
                # spaces after this gap
                spaces = base_spaces + (1 if k < extra else 0)
                parts.append(' ' * spaces)
            parts.append(words[j-1])
            line = ''.join(parts)
        res.append(line)
        i = j
    return res
