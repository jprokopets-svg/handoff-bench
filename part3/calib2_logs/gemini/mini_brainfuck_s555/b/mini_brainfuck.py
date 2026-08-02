def brainfuck(code: str, input_str: str = "") -> str:
    tape = [0] * 30000
    data_ptr = 0
    code_ptr = 0
    output = []
    input_ptr = 0

    # Pre-process the code to find matching brackets
    bracket_map = {}
    temp_bracket_stack = []
    for i, char in enumerate(code):
        if char == '[':
            temp_bracket_stack.append(i)
        elif char == ']':
            if not temp_bracket_stack:
                raise ValueError("Unbalanced brackets")
            open_bracket_pos = temp_bracket_stack.pop()
            bracket_map[open_bracket_pos] = i
            bracket_map[i] = open_bracket_pos
    if temp_bracket_stack:
        raise ValueError("Unbalanced brackets")

    while code_ptr < len(code):
        command = code[code_ptr]

        if command == '>':
            data_ptr += 1
        elif command == '<':
            data_ptr -= 1
        elif command == '+':
            tape[data_ptr] += 1
        elif command == '-':
            tape[data_ptr] -= 1
        elif command == '.':
            output.append(chr(tape[data_ptr]))
        elif command == ',':
            if input_ptr < len(input_str):
                tape[data_ptr] = ord(input_str[input_ptr])
                input_ptr += 1
            else:
                tape[data_ptr] = 0
        elif command == '[':
            if tape[data_ptr] == 0:
                code_ptr = bracket_map[code_ptr]
        elif command == ']':
            if tape[data_ptr] != 0:
                code_ptr = bracket_map[code_ptr]
        
        code_ptr += 1
    return "".join(output)
