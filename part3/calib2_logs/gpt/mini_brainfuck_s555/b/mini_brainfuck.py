def brainfuck(code: str, input_str: str = "") -> str:
    # Precompute bracket matches
    stack = []
    matches = {}
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            if not stack:
                raise ValueError("Unmatched closing bracket")
            j = stack.pop()
            matches[i] = j
            matches[j] = i
    if stack:
        # there are unmatched opening brackets
        raise ValueError("Unmatched opening bracket")

    tape = [0] * 30000
    ptr = 0
    pc = 0
    output_chars = []
    inp_idx = 0
    n = len(code)

    while pc < n:
        cmd = code[pc]
        if cmd == ">":
            ptr += 1
            if ptr >= len(tape) or ptr < 0:
                raise IndexError("Pointer moved out of tape bounds")
            pc += 1
        elif cmd == "<":
            ptr -= 1
            if ptr < 0 or ptr >= len(tape):
                raise IndexError("Pointer moved out of tape bounds")
            pc += 1
        elif cmd == "+":
            tape[ptr] += 1
            pc += 1
        elif cmd == "-":
            tape[ptr] -= 1
            pc += 1
        elif cmd == ".":
            output_chars.append(chr(tape[ptr]))
            pc += 1
        elif cmd == ",":
            if inp_idx < len(input_str):
                tape[ptr] = ord(input_str[inp_idx])
                inp_idx += 1
            else:
                tape[ptr] = 0
            pc += 1
        elif cmd == "[":
            if tape[ptr] == 0:
                # jump to after matching ]
                pc = matches[pc] + 1
            else:
                pc += 1
        elif cmd == "]":
            if tape[ptr] != 0:
                # jump back to just after matching [
                pc = matches[pc] + 1
            else:
                pc += 1
        else:
            # ignore any other character
            pc += 1

    return "".join(output_chars)
