def brainfuck(code: str, input_str: str = "") -> str:
    # Initialize tape with 30,000 cells
    tape = [0] * 30000
    ptr = 0  # data pointer
    input_ptr = 0  # input pointer
    output = []
    
    # Preprocess to find matching brackets
    stack = []
    bracket_map = {}
    
    for i, ch in enumerate(code):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            if not stack:
                raise ValueError("Unbalanced brackets")
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start
    
    if stack:
        raise ValueError("Unbalanced brackets")
    
    # Execute the code
    i = 0
    while i < len(code):
        ch = code[i]
        
        if ch == '>':
            ptr += 1
            if ptr >= len(tape):
                # Could extend tape if needed, but spec says 30,000 cells
                # We'll just stay at the end
                ptr = len(tape) - 1
        elif ch == '<':
            ptr -= 1
            if ptr < 0:
                ptr = 0
        elif ch == '+':
            tape[ptr] += 1
        elif ch == '-':
            tape[ptr] -= 1
        elif ch == '.':
            output.append(chr(tape[ptr]))
        elif ch == ',':
            if input_ptr < len(input_str):
                tape[ptr] = ord(input_str[input_ptr])
                input_ptr += 1
            else:
                tape[ptr] = 0
        elif ch == '[':
            if tape[ptr] == 0:
                i = bracket_map[i]  # jump to matching ']'
        elif ch == ']':
            if tape[ptr] != 0:
                i = bracket_map[i]  # jump back to matching '['
        
        i += 1
    
    return ''.join(output)