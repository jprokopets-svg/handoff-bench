def brainfuck(code: str, input_str: str = "") -> str:
    """
    Execute a Brainfuck program given by `code` with optional input string `input_str`.

    Tape: 30,000 cells initialized to 0. Cells are Python ints with NO wraparound.
    Data pointer starts at 0. Allowed commands: > < + - . , [ ]
    Any other characters are ignored.

    For ',' reads the next character from input_str and stores its ord() value in the current cell;
    if input is exhausted stores 0.

    For '.' appends chr(current cell) to output (may raise if value outside valid range).

    Raises ValueError if brackets are unbalanced.
    """
    # Precompute matching brackets
    open_stack = []
    jump = {}
    for i, ch in enumerate(code):
        if ch == '[':
            open_stack.append(i)
        elif ch == ']':
            if not open_stack:
                raise ValueError("Unmatched closing bracket at position {}".format(i))
            j = open_stack.pop()
            jump[j] = i
            jump[i] = j
    if open_stack:
        # unmatched opening bracket(s)
        raise ValueError("Unmatched opening bracket(s)")

    tape = [0] * 30000
    dp = 0  # data pointer
    ip = 0  # instruction pointer
    inp_pos = 0
    output_chars = []
    n = len(code)

    while ip < n:
        cmd = code[ip]
        if cmd == '>':
            dp += 1
            if dp >= len(tape) or dp < 0:
                raise IndexError("Data pointer moved out of tape bounds")
        elif cmd == '<':
            dp -= 1
            if dp >= len(tape) or dp < 0:
                raise IndexError("Data pointer moved out of tape bounds")
        elif cmd == '+':
            tape[dp] += 1
        elif cmd == '-':
            tape[dp] -= 1
        elif cmd == '.':
            output_chars.append(chr(tape[dp]))
        elif cmd == ',':
            if inp_pos < len(input_str):
                tape[dp] = ord(input_str[inp_pos])
                inp_pos += 1
            else:
                tape[dp] = 0
        elif cmd == '[':
            if tape[dp] == 0:
                # jump forward to matching ] (jump maps [->])
                ip = jump[ip]
        elif cmd == ']':
            if tape[dp] != 0:
                # jump back to matching [ (jump maps ]->[), then continue from after it
                ip = jump[ip]
        # ignore any other characters
        ip += 1
    return ''.join(output_chars)
