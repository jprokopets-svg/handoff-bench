def brainfuck(code: str, input_str: str = "") -> str:
    # Initialize tape with 30,000 cells
    tape = [0] * 30000
    pointer = 0
    input_index = -1  # Start before first character
    output = []
    
    # Preprocess to find matching brackets
    stack = []
    bracket_map = {}
    
    # First pass: build bracket map and check for unbalanced brackets
    for i, char in enumerate(code):
        if char == '[':
            stack.append(i)
        elif char == ']':
            if not stack:
                raise ValueError("Unbalanced brackets")
            open_idx = stack.pop()
            bracket_map[open_idx] = i
            bracket_map[i] = open_idx
    
    # If stack not empty after processing, brackets are unbalanced
    if stack:
        raise ValueError("Unbalanced brackets")
    
    # Execute the code
    i = 0
    while i < len(code):
        char = code[i]
        
        if char == '>':
            pointer += 1
            if pointer >= 30000:
                pointer = 29999  # Stay within bounds
        elif char == '<':
            pointer -= 1
            if pointer < 0:
                pointer = 0  # Stay within bounds
        elif char == '+':
            tape[pointer] += 1
            # No wraparound - just keep incrementing
        elif char == '-':
            tape[pointer] -= 1
            # No wraparound - just keep decrementing
        elif char == '.':
            output.append(chr(tape[pointer]))
        elif char == ',':
            input_index += 1
            if input_index < len(input_str):
                tape[pointer] = ord(input_str[input_index])
            else:
                tape[pointer] = 0  # EOF -> 0
        elif char == '[':
            if tape[pointer] == 0:
                # Jump forward to matching ']'
                i = bracket_map[i]
        elif char == ']':
            if tape[pointer] != 0:
                # Jump back to matching '['
                i = bracket_map[i]
        # Other characters are ignored
        
        i += 1
    
    return ''.join(output)