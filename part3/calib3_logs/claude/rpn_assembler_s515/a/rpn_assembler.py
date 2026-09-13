def run_asm(src: str) -> str:
    # Parse the source code
    lines = src.split('\n')
    instructions = []
    labels = {}
    
    # First pass: parse instructions and collect labels
    for line in lines:
        # Remove comments
        if '#' in line:
            line = line[:line.index('#')]
        
        line = line.strip()
        
        # Skip blank lines
        if not line:
            continue
        
        # Check if it's a label
        if line.endswith(':'):
            label_name = line[:-1].strip()
            if not label_name.isidentifier():
                raise ValueError(f"Invalid label name: {label_name}")
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            labels[label_name] = len(instructions)
            continue
        
        instructions.append(line)
    
    # Execute the program
    stack = []
    output = []
    pc = 0  # program counter
    
    while pc < len(instructions):
        instr = instructions[pc]
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
                raise ValueError(f"PUSH operand must be an integer")
            stack.append(value)
        
        elif mnemonic == 'POP':
            if len(parts) != 1:
                raise ValueError(f"POP takes no operands")
            if len(stack) < 1:
                raise ValueError(f"Stack underflow")
            stack.pop()
        
        elif mnemonic == 'DUP':
            if len(parts) != 1:
                raise ValueError(f"DUP takes no operands")
            if len(stack) < 1:
                raise ValueError(f"Stack underflow")
            stack.append(stack[-1])
        
        elif mnemonic == 'SWAP':
            if len(parts) != 1:
                raise ValueError(f"SWAP takes no operands")
            if len(stack) < 2:
                raise ValueError(f"Stack underflow")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        
        elif mnemonic == 'ADD':
            if len(parts) != 1:
                raise ValueError(f"ADD takes no operands")
            if len(stack) < 2:
                raise ValueError(f"Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        
        elif mnemonic == 'SUB':
            if len(parts) != 1:
                raise ValueError(f"SUB takes no operands")
            if len(stack) < 2:
                raise ValueError(f"Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        
        elif mnemonic == 'MUL':
            if len(parts) != 1:
                raise ValueError(f"MUL takes no operands")
            if len(stack) < 2:
                raise ValueError(f"Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        
        elif mnemonic == 'DIV':
            if len(parts) != 1:
                raise ValueError(f"DIV takes no operands")
            if len(stack) < 2:
                raise ValueError(f"Stack underflow")
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ValueError(f"Division by zero")
            stack.append(a // b)
        
        elif mnemonic == 'NEG':
            if len(parts) != 1:
                raise ValueError(f"NEG takes no operands")
            if len(stack) < 1:
                raise ValueError(f"Stack underflow")
            stack[-1] = -stack[-1]
        
        elif mnemonic == 'PRINT':
            if len(parts) != 1:
                raise ValueError(f"PRINT takes no operands")
            if len(stack) < 1:
                raise ValueError(f"Stack underflow")
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
                raise ValueError(f"Stack underflow")
            value = stack.pop()
            label = parts[1]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            if value == 0:
                pc = labels[label]
                continue
        
        elif mnemonic == 'JNZ':
            if len(parts) != 2:
                raise ValueError(f"JNZ requires exactly one operand")
            if len(stack) < 1:
                raise ValueError(f"Stack underflow")
            value = stack.pop()
            label = parts[1]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            if value != 0:
                pc = labels[label]
                continue
        
        else:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")
        
        pc += 1
    
    return ''.join(output)
