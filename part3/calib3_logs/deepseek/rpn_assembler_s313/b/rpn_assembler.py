def run_asm(src: str) -> str:
    # First pass: collect labels and their line numbers
    lines = src.splitlines()
    labels = {}
    instructions = []
    
    # Filter out comments and blank lines, track line numbers
    line_num = 0
    for line in lines:
        # Strip leading/trailing whitespace
        line = line.strip()
        # Remove comment part
        if '#' in line:
            line = line[:line.index('#')].strip()
        # Skip empty lines
        if not line:
            continue
            
        # Check if it's a label definition
        if line.endswith(':'):
            label_name = line[:-1].strip()
            if not label_name:
                continue
            # Validate label name (alphanumeric + underscore)
            if not all(c.isalnum() or c == '_' for c in label_name):
                raise ValueError("Invalid label name")
            if label_name in labels:
                raise ValueError("Duplicate label")
            labels[label_name] = line_num  # Label points to next instruction
        else:
            # It's an instruction, will be processed in second pass
            line_num += 1
    
    # Second pass: parse instructions
    line_num = 0
    for line in lines:
        line = line.strip()
        if '#' in line:
            line = line[:line.index('#')].strip()
        if not line:
            continue
            
        # Skip label definitions in second pass
        if line.endswith(':'):
            continue
            
        # Parse instruction
        parts = line.split()
        if not parts:
            continue
            
        mnemonic = parts[0].upper()
        
        # Validate mnemonic
        valid_mnemonics = {'PUSH', 'POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 
                          'NEG', 'PRINT', 'HALT', 'JMP', 'JZ', 'JNZ'}
        if mnemonic not in valid_mnemonics:
            raise ValueError("Unknown mnemonic")
        
        # Validate operand count
        if mnemonic == 'PUSH':
            if len(parts) != 2:
                raise ValueError("Wrong operand count")
            try:
                operand = int(parts[1])
            except ValueError:
                raise ValueError("Non-integer PUSH")
            instructions.append((mnemonic, operand))
        elif mnemonic in {'JMP', 'JZ', 'JNZ'}:
            if len(parts) != 2:
                raise ValueError("Wrong operand count")
            label_name = parts[1]
            # Store label name for later resolution
            instructions.append((mnemonic, label_name))
        else:
            # Instructions without operands
            if len(parts) != 1:
                raise ValueError("Wrong operand count")
            instructions.append((mnemonic, None))
        
        line_num += 1
    
    # Resolve jump labels
    resolved_instructions = []
    for mnemonic, operand in instructions:
        if mnemonic in {'JMP', 'JZ', 'JNZ'}:
            if operand not in labels:
                raise ValueError("Undefined label")
            resolved_instructions.append((mnemonic, labels[operand]))
        else:
            resolved_instructions.append((mnemonic, operand))
    
    # Execute program
    stack = []
    output = []
    pc = 0  # program counter
    
    while pc < len(resolved_instructions):
        mnemonic, operand = resolved_instructions[pc]
        pc += 1
        
        if mnemonic == 'PUSH':
            stack.append(operand)
        elif mnemonic == 'POP':
            if not stack:
                raise ValueError("Stack underflow")
            stack.pop()
        elif mnemonic == 'DUP':
            if not stack:
                raise ValueError("Stack underflow")
            stack.append(stack[-1])
        elif mnemonic == 'SWAP':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif mnemonic == 'ADD':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif mnemonic == 'SUB':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif mnemonic == 'MUL':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif mnemonic == 'DIV':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ValueError("Division by zero")
            stack.append(a // b)
        elif mnemonic == 'NEG':
            if not stack:
                raise ValueError("Stack underflow")
            stack[-1] = -stack[-1]
        elif mnemonic == 'PRINT':
            if not stack:
                raise ValueError("Stack underflow")
            value = stack.pop()
            output.append(str(value) + '\n')
        elif mnemonic == 'HALT':
            break
        elif mnemonic == 'JMP':
            pc = operand
        elif mnemonic == 'JZ':
            if not stack:
                raise ValueError("Stack underflow")
            value = stack.pop()
            if value == 0:
                pc = operand
        elif mnemonic == 'JNZ':
            if not stack:
                raise ValueError("Stack underflow")
            value = stack.pop()
            if value != 0:
                pc = operand
    
    return ''.join(output)