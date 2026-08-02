def brainfuck(code: str, input_str: str = "") -> str:
    # Initialize tape with 30,000 cells
    tape = [0] * 30000
    pointer = 0
    input_index = 0
    output = []
    
    # Preprocess to find matching brackets
    stack = []
    bracket_map = {}
    
    for i, char in enumerate(code):
        if char == '[':
            stack.append(i)
        elif char == ']':
            if not stack:
                raise ValueError("Unbalanced brackets")
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start
    
    # Check for unmatched brackets
    if stack:
        raise ValueError("Unbalanced brackets")
    
    # Execute the code
    i = 0
    while i < len(code):
        char = code[i]
        
        if char == '>':
            pointer = (pointer + 1) % 30000
        elif char == '<':
            pointer = (pointer - 1) % 30000
        elif char == '+':
            tape[pointer] += 1
        elif char == '-':
            tape[pointer] -= 1
        elif char == '.':
            output.append(chr(tape[pointer]))
        elif char == ',':
            if input_index < len(input_str):
                tape[pointer] = ord(input_str[input_index])
                input_index += 1
            else:
                tape[pointer] = -1  # Set to -1 for EOF
        elif char == '[':
            if tape[pointer] == 0:
                i = bracket_map[i]
        elif char == ']':
            if tape[pointer] != 0:
                i = bracket_map[i]
        # Other characters are ignored
        
        i += 1
    
    return ''.join(output)