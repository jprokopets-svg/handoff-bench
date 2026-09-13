def run_asm(src: str) -> str:
    """
    Assembles and executes a stack-machine program.
    Returns the concatenation of all PRINTED values (each followed by newline).
    """
    # Parse the source code into lines
    lines = src.split('\n')
    
    # Strip comments and whitespace, skip blank lines
    instructions = []
    for line in lines:
        # Remove comments
        if '#' in line:
            line = line[:line.index('#')]
        line = line.strip()
        if line:
            instructions.append(line)
    
    # First pass: collect labels
    labels = {}  # label_name -> instruction_index
    processed_instructions = []
    
    for instr in instructions:
        if instr.endswith(':'):
            # This is a label definition
            label_name = instr[:-1].strip()
            # Validate label name (alphanumeric + underscore)
            if not all(c.isalnum() or c == '_' for c in label_name):
                raise ValueError(f"Invalid label name: {label_name}")
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            labels[label_name] = len(processed_instructions)
        else:
            processed_instructions.append(instr)
    
    # Second pass: execute instructions
    stack = []
    output = []
    pc = 0  # program counter
    
    while pc < len(processed_instructions):
        instr = processed_instructions[pc]
        parts = instr.split()
        
        if not parts:
            pc += 1
            continue
        
        mnemonic = parts[0]
        
        if mnemonic == 'PUSH':
            if len(parts) != 2:
                raise ValueError(f"PUSH requires exactly one operand")
            try:
                value = int(parts[1])
            except ValueError:
                raise ValueError(f"PUSH operand must be an integer: {parts[1]}")
            stack.append(value)
        
        elif mnemonic == 'POP':
            if len(parts) != 1:
                raise ValueError(f"POP takes no operands")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.pop()
        
        elif mnemonic == 'DUP':
            if len(parts) != 1:
                raise ValueError(f"DUP takes no operands")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.append(stack[-1])
        
        elif mnemonic == 'SWAP':
            if len(parts) != 1:
                raise ValueError(f"SWAP takes no operands")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        
        elif mnemonic == 'ADD':
            if len(parts) != 1:
                raise ValueError(f"ADD takes no operands")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        
        elif mnemonic == 'SUB':
            if len(parts) != 1:
                raise ValueError(f"SUB takes no operands")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        
        elif mnemonic == 'MUL':
            if len(parts) != 1:
                raise ValueError(f"MUL takes no operands")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        
        elif mnemonic == 'DIV':
            if len(parts) != 1:
                raise ValueError(f"DIV takes no operands")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ValueError("Division by zero")
            stack.append(a // b)
        
        elif mnemonic == 'NEG':
            if len(parts) != 1:
                raise ValueError(f"NEG takes no operands")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack[-1] = -stack[-1]
        
        elif mnemonic == 'PRINT':
            if len(parts) != 1:
                raise ValueError(f"PRINT takes no operands")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            output.append(str(value) + '\n')
        
        elif mnemonic == 'HALT':
            if len(parts) != 1:
                raise ValueError(f"HALT takes no operands")
            break
        
        elif mnemonic == 'JMP':
            if len(parts) != 2:
                raise ValueError(f"JMP requires exactly one operand")
            label = parts[1]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            pc = labels[label]
            continue
        
        elif mnemonic == 'JZ':
            if len(parts) != 2:
                raise ValueError(f"JZ requires exactly one operand")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            if value == 0:
                label = parts[1]
                if label not in labels:
                    raise ValueError(f"Undefined label: {label}")
                pc = labels[label]
                continue
        
        elif mnemonic == 'JNZ':
            if len(parts) != 2:
                raise ValueError(f"JNZ requires exactly one operand")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            if value != 0:
                label = parts[1]
                if label not in labels:
                    raise ValueError(f"Undefined label: {label}")
                pc = labels[label]
                continue
        
        else:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")
        
        pc += 1
    
    return ''.join(output)
