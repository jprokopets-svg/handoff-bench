def brainfuck(code: str, input_str: str = "") -> str:
    # Initialize tape with 30,000 cells
    tape = [0] * 30000
    data_ptr = 0
    code_ptr = 0
    input_ptr = 0
    output = []
    
    # First, validate and build bracket map
    bracket_map = {}
    bracket_stack = []
    
    for i, char in enumerate(code):
        if char == '[':
            bracket_stack.append(i)
        elif char == ']':
            if not bracket_stack:
                raise ValueError("Unbalanced brackets: ] without matching [")
            left = bracket_stack.pop()
            bracket_map[left] = i
            bracket_map[i] = left
    
    if bracket_stack:
        raise ValueError("Unbalanced brackets: [ without matching ]")
    
    # Execute the code
    while code_ptr < len(code):
        char = code[code_ptr]
        
        if char == '>':
            data_ptr += 1
            if data_ptr >= 30000:
                data_ptr = 30000 - 1  # Clamp to tape size
        elif char == '<':
            data_ptr -= 1
            if data_ptr < 0:
                data_ptr = 0  # Clamp to tape start
        elif char == '+':
            tape[data_ptr] += 1
        elif char == '-':
            tape[data_ptr] -= 1
        elif char == '.':
            output.append(chr(tape[data_ptr]))
        elif char == ',':
            if input_ptr < len(input_str):
                tape[data_ptr] = ord(input_str[input_ptr])
                input_ptr += 1
            else:
                tape[data_ptr] = 0
        elif char == '[':
            if tape[data_ptr] == 0:
                code_ptr = bracket_map[code_ptr]
        elif char == ']':
            if tape[data_ptr] != 0:
                code_ptr = bracket_map[code_ptr]
        
        code_ptr += 1
    
    return ''.join(output)
