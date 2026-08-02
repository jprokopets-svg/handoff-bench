def brainfuck(code: str, input_str: str = "") -> str:
    # Initialize tape with 30,000 cells
    tape = [0] * 30000
    ptr = 0  # data pointer
    ip = 0   # instruction pointer
    input_ptr = 0  # input pointer
    output = []
    
    # Preprocess brackets for O(1) jumps
    stack = []
    jump_map = {}
    
    # Build jump map for matching brackets
    for i, ch in enumerate(code):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            if not stack:
                raise ValueError("Unbalanced brackets")
            start = stack.pop()
            jump_map[start] = i
            jump_map[i] = start
    
    # Check for unmatched opening brackets
    if stack:
        raise ValueError("Unbalanced brackets")
    
    # Execute the program
    while ip < len(code):
        ch = code[ip]
        
        if ch == '>':
            ptr += 1
            if ptr >= 30000:
                ptr = 0  # wrap around? The spec says tape has 30,000 cells, 
                         # but doesn't specify wrap. We'll assume pointer stays within bounds.
                         # Actually, typical Brainfuck implementations wrap or error.
                         # Let's keep within bounds.
                ptr = 29999  # or we could wrap to 0, but let's stay at last cell
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
                ip = jump_map[ip]  # jump to matching ']'
        elif ch == ']':
            if tape[ptr] != 0:
                ip = jump_map[ip]  # jump back to matching '['
        
        ip += 1
    
    return ''.join(output)