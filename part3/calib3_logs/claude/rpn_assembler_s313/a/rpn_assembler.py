def run_asm(src: str) -> str:
    # Parse the source code
    lines = src.split('\n')
    instructions = []
    labels = {}
    
    # First pass: parse instructions and collect labels
    for line_num, line in enumerate(lines):
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
            # Validate label name (alphanumeric + underscore)
            if not all(c.isalnum() or c == '_' for c in label_name):
                raise ValueError(f"Invalid label name: {label_name}")
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            labels[label_name] = len(instructions)
            continue
        
        # Parse instruction
        parts = line.split()
        if not parts:
            continue
        
        mnemonic = parts[0]
        operands = parts[1:]
        
        instructions.append((mnemonic, operands))
    
    # Validate all labels are defined for jumps
    for mnemonic, operands in instructions:
        if mnemonic in ('JMP', 'JZ', 'JNZ'):
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for {mnemonic}")
            if operands[0] not in labels:
                raise ValueError(f"Undefined label: {operands[0]}")
    
    # Execute the program
    stack = []
    output = []
    pc = 0  # program counter
    
    while pc < len(instructions):
        mnemonic, operands = instructions[pc]
        
        if mnemonic == 'PUSH':
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for PUSH")
            try:
                value = int(operands[0])
            except ValueError:
                raise ValueError(f"Non-integer PUSH operand: {operands[0]}")
            stack.append(value)
            pc += 1
        
        elif mnemonic == 'POP':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for POP")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.pop()
            pc += 1
        
        elif mnemonic == 'DUP':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for DUP")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.append(stack[-1])
            pc += 1
        
        elif mnemonic == 'SWAP':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for SWAP")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            stack[-1], stack[-2] = stack[-2], stack[-1]
            pc += 1
        
        elif mnemonic == 'ADD':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for ADD")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
            pc += 1
        
        elif mnemonic == 'SUB':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for SUB")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
            pc += 1
        
        elif mnemonic == 'MUL':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for MUL")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
            pc += 1
        
        elif mnemonic == 'DIV':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for DIV")
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ValueError("Division by zero")
            stack.append(a // b)
            pc += 1
        
        elif mnemonic == 'NEG':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for NEG")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack[-1] = -stack[-1]
            pc += 1
        
        elif mnemonic == 'PRINT':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for PRINT")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            output.append(str(value) + '\n')
            pc += 1
        
        elif mnemonic == 'HALT':
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for HALT")
            break
        
        elif mnemonic == 'JMP':
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for JMP")
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            pc = labels[label]
        
        elif mnemonic == 'JZ':
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for JZ")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            if value == 0:
                pc = labels[label]
            else:
                pc += 1
        
        elif mnemonic == 'JNZ':
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for JNZ")
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            if value != 0:
                pc = labels[label]
            else:
                pc += 1
        
        else:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")
    
    return ''.join(output)
