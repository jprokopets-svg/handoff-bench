def brainfuck(code, input_str=""):
    tape = [0] * 30000
    data_ptr = 0
    input_ptr = 0
    output = []
    code_ptr = 0
    
    # Pre-process the code to find matching brackets
    bracket_map = {}
    open_brackets = []
    for i, char in enumerate(code):
        if char == '[':
            open_brackets.append(i)
        elif char == ']':
            if not open_brackets:
                raise ValueError("Unbalanced brackets")
            open = open_brackets.pop()
            bracket_map[open] = i
            bracket_map[i] = open
    if open_brackets:
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
