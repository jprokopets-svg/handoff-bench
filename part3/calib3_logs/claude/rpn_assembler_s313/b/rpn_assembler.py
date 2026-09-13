def run_asm(src: str) -> str:
    # Parse the source code
    lines = src.split('\n')
    
    # First pass: collect labels and clean instructions
    instructions = []
    labels = {}
    
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
            if not label_name:
                raise ValueError("Empty label name")
            if not all(c.isalnum() or c == '_' for c in label_name):
                raise ValueError(f"Invalid label name: {label_name}")
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            labels[label_name] = len(instructions)
        else:
            instructions.append(line)
    
    # Second pass: parse and validate instructions
    parsed_instructions = []
    for instr in instructions:
        tokens = instr.split()
        if not tokens:
            continue
        
        mnemonic = tokens[0]
        operands = tokens[1:]
        
        # Validate instruction
        if mnemonic == 'PUSH':
            if len(operands) != 1:
                raise ValueError(f"PUSH requires exactly 1 operand, got {len(operands)}")
            try:
                value = int(operands[0])
            except ValueError:
                raise ValueError(f"PUSH operand must be an integer, got {operands[0]}")
            parsed_instructions.append(('PUSH', value))
        
        elif mnemonic == 'POP':
            if len(operands) != 0:
                raise ValueError(f"POP requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('POP',))
        
        elif mnemonic == 'DUP':
            if len(operands) != 0:
                raise ValueError(f"DUP requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('DUP',))
        
        elif mnemonic == 'SWAP':
            if len(operands) != 0:
                raise ValueError(f"SWAP requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('SWAP',))
        
        elif mnemonic == 'ADD':
            if len(operands) != 0:
                raise ValueError(f"ADD requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('ADD',))
        
        elif mnemonic == 'SUB':
            if len(operands) != 0:
                raise ValueError(f"SUB requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('SUB',))
        
        elif mnemonic == 'MUL':
            if len(operands) != 0:
                raise ValueError(f"MUL requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('MUL',))
        
        elif mnemonic == 'DIV':
            if len(operands) != 0:
                raise ValueError(f"DIV requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('DIV',))
        
        elif mnemonic == 'NEG':
            if len(operands) != 0:
                raise ValueError(f"NEG requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('NEG',))
        
        elif mnemonic == 'PRINT':
            if len(operands) != 0:
                raise ValueError(f"PRINT requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('PRINT',))
        
        elif mnemonic == 'HALT':
            if len(operands) != 0:
                raise ValueError(f"HALT requires 0 operands, got {len(operands)}")
            parsed_instructions.append(('HALT',))
        
        elif mnemonic == 'JMP':
            if len(operands) != 1:
                raise ValueError(f"JMP requires exactly 1 operand, got {len(operands)}")
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            parsed_instructions.append(('JMP', labels[label]))
        
        elif mnemonic == 'JZ':
            if len(operands) != 1:
                raise ValueError(f"JZ requires exactly 1 operand, got {len(operands)}")
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            parsed_instructions.append(('JZ', labels[label]))
        
        elif mnemonic == 'JNZ':
            if len(operands) != 1:
                raise ValueError(f"JNZ requires exactly 1 operand, got {len(operands)}")
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            parsed_instructions.append(('JNZ', labels[label]))
        
        else:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")
    
    # Execute the program
    stack = []
    output = []
    pc = 0  # program counter
    
    while pc < len(parsed_instructions):
        instr = parsed_instructions[pc]
        mnemonic = instr[0]
        
        if mnemonic == 'PUSH':
            stack.append(instr[1])
            pc += 1
        
        elif mnemonic == 'POP':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.pop()
            pc += 1
        
        elif mnemonic == 'DUP':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.append(stack[-1])
            pc += 1
        
        elif mnemonic == 'SWAP':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            stack[-1], stack[-2] = stack[-2], stack[-1]
            pc += 1
        
        elif mnemonic == 'ADD':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
            pc += 1
        
        elif mnemonic == 'SUB':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
            pc += 1
        
        elif mnemonic == 'MUL':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
            pc += 1
        
        elif mnemonic == 'DIV':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ValueError("Division by zero")
            stack.append(a // b)
            pc += 1
        
        elif mnemonic == 'NEG':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.append(-stack.pop())
            pc += 1
        
        elif mnemonic == 'PRINT':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            output.append(str(value) + '\n')
            pc += 1
        
        elif mnemonic == 'HALT':
            break
        
        elif mnemonic == 'JMP':
            pc = instr[1]
        
        elif mnemonic == 'JZ':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            if value == 0:
                pc = instr[1]
            else:
                pc += 1
        
        elif mnemonic == 'JNZ':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            value = stack.pop()
            if value != 0:
                pc = instr[1]
            else:
                pc += 1
    
    return ''.join(output)
