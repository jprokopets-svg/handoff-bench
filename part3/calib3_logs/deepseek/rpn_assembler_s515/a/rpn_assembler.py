def run_asm(src: str) -> str:
    """Assemble and execute the program, return printed output."""
    # Parse source code
    lines = src.strip().splitlines()
    instructions = []
    labels = {}
    output_lines = []
    
    # First pass: collect labels and build instruction list
    for line_num, line in enumerate(lines):
        # Strip whitespace and handle comments
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Check for label definition
        if line.endswith(':'):
            label_name = line[:-1].strip()
            if not label_name.replace('_', '').isalnum():
                raise ValueError(f"Invalid label name: {label_name}")
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            labels[label_name] = len(instructions)  # Label points to next instruction
            continue
            
        # Parse instruction
        parts = line.split()
        if not parts:
            continue
            
        mnemonic = parts[0].upper()
        operand = None
        if len(parts) > 1:
            # Join remaining parts for operand (though typically just one)
            operand = ' '.join(parts[1:])
        
        instructions.append((mnemonic, operand))
    
    # Second pass: resolve labels and execute
    pc = 0  # Program counter
    stack = []
    output = []
    halted = False
    
    while pc < len(instructions) and not halted:
        mnemonic, operand = instructions[pc]
        pc += 1
        
        try:
            if mnemonic == 'PUSH':
                if operand is None:
                    raise ValueError("PUSH requires an operand")
                try:
                    value = int(operand)
                except ValueError:
                    raise ValueError(f"Invalid integer for PUSH: {operand}")
                stack.append(value)
                
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
                halted = True
                
            elif mnemonic == 'JMP':
                if operand is None:
                    raise ValueError("JMP requires a label")
                if operand not in labels:
                    raise ValueError(f"Undefined label: {operand}")
                pc = labels[operand]
                
            elif mnemonic == 'JZ':
                if operand is None:
                    raise ValueError("JZ requires a label")
                if not stack:
                    raise ValueError("Stack underflow")
                value = stack.pop()
                if value == 0:
                    if operand not in labels:
                        raise ValueError(f"Undefined label: {operand}")
                    pc = labels[operand]
                    
            elif mnemonic == 'JNZ':
                if operand is None:
                    raise ValueError("JNZ requires a label")
                if not stack:
                    raise ValueError("Stack underflow")
                value = stack.pop()
                if value != 0:
                    if operand not in labels:
                        raise ValueError(f"Undefined label: {operand}")
                    pc = labels[operand]
                    
            else:
                raise ValueError(f"Unknown mnemonic: {mnemonic}")
                
        except ValueError as e:
            # Re-raise ValueError for both assembly and runtime errors
            raise ValueError(str(e))
    
    return ''.join(output)