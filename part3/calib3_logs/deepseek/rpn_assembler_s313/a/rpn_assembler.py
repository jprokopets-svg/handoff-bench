def run_asm(src: str) -> str:
    """Assemble and execute the program, return printed output."""
    # Parse source
    lines = src.splitlines()
    instructions = []
    labels = {}
    output_lines = []
    
    # First pass: collect labels and build instruction list
    line_num = 0
    for line in lines:
        # Strip whitespace
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        # Remove comments
        if '#' in line:
            line = line[:line.index('#')].strip()
            if not line:
                continue
        # Check for label
        if line.endswith(':'):
            label_name = line[:-1].strip()
            if not label_name.replace('_', '').isalnum():
                raise ValueError(f"Invalid label name: {label_name}")
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            labels[label_name] = line_num
            continue
        
        # Parse instruction
        parts = line.split()
        if not parts:
            continue
        mnemonic = parts[0]
        operands = parts[1:]
        
        # Validate instruction
        if mnemonic not in {'PUSH', 'POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 
                           'NEG', 'PRINT', 'HALT', 'JMP', 'JZ', 'JNZ'}:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")
        
        # Validate operand count
        if mnemonic in {'PUSH', 'JMP', 'JZ', 'JNZ'}:
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for {mnemonic}")
        else:
            if operands:
                raise ValueError(f"Wrong operand count for {mnemonic}")
        
        # For PUSH, validate integer
        if mnemonic == 'PUSH':
            try:
                value = int(operands[0])
            except ValueError:
                raise ValueError(f"Non-integer PUSH: {operands[0]}")
            instructions.append((mnemonic, value))
        else:
            instructions.append((mnemonic, operands[0] if operands else None))
        
        line_num += 1
    
    # Second pass: resolve labels and execute
    pc = 0  # program counter
    stack = []
    output = []
    halted = False
    
    while pc < len(instructions):
        mnemonic, operand = instructions[pc]
        
        if halted:
            break
            
        if mnemonic == 'HALT':
            halted = True
            pc += 1
            continue
        
        # Handle jumps first (they don't use stack)
        if mnemonic in {'JMP', 'JZ', 'JNZ'}:
            if operand not in labels:
                raise ValueError(f"Undefined label: {operand}")
            target = labels[operand]
            
            if mnemonic == 'JMP':
                pc = target
                continue
            elif mnemonic == 'JZ':
                if not stack:
                    raise ValueError("Stack underflow")
                value = stack.pop()
                if value == 0:
                    pc = target
                    continue
            elif mnemonic == 'JNZ':
                if not stack:
                    raise ValueError("Stack underflow")
                value = stack.pop()
                if value != 0:
                    pc = target
                    continue
        
        # Stack operations
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
        
        pc += 1
    
    return ''.join(output)