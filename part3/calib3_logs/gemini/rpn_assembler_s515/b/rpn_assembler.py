
import re

def run_asm(src: str) -> str:
    # --- Pass 1: Parse and find labels ---
    labels = {}
    program_lines = []
    lines = src.split('\n')
    for line in lines:
        # Strip comments and whitespace
        if '#' in line:
            line = line[:line.find('#')]
        line = line.strip()
        if not line:
            continue

        if line.endswith(':'):
            label = line[:-1]
            if not re.match(r'^[a-zA-Z0-9_]+$', label):
                 raise ValueError(f"Invalid label name: {label}")
            if label in labels:
                raise ValueError(f"Duplicate label: {label}")
            labels[label] = len(program_lines)
        else:
            program_lines.append(line)

    # --- Pass 2: Assemble the program ---
    program = []
    for line in program_lines:
        parts = line.split()
        mnemonic = parts[0].upper()
        operands = parts[1:]

        if mnemonic == 'PUSH':
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for PUSH: {line}")
            try:
                val = int(operands[0])
                program.append(('PUSH', val))
            except ValueError:
                raise ValueError(f"Non-integer PUSH operand: {operands[0]}")
        elif mnemonic in ['POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 'NEG', 'PRINT', 'HALT']:
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for {mnemonic}: {line}")
            program.append((mnemonic,))
        elif mnemonic in ['JMP', 'JZ', 'JNZ']:
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for {mnemonic}: {line}")
            label = operands[0]
            program.append((mnemonic, label))
        else:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")

    # Resolve labels in the program
    for i, instruction in enumerate(program):
        mnemonic = instruction[0]
        if mnemonic in ['JMP', 'JZ', 'JNZ']:
            label = instruction[1]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            program[i] = (mnemonic, labels[label])

    # --- Simulation ---
    stack = []
    pc = 0
    output = ""
    
    # Limit execution steps to prevent infinite loops in tests
    max_steps = 10000 
    steps = 0

    while 0 <= pc < len(program) and steps < max_steps:
        instruction = program[pc]
        mnemonic = instruction[0]
        
        pc_increment = 1

        if mnemonic == 'PUSH':
            stack.append(instruction[1])
        elif mnemonic == 'POP':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.pop()
        elif mnemonic == 'DUP':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack.append(stack[-1])
        elif mnemonic == 'SWAP':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
        elif mnemonic == 'ADD':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
        elif mnemonic == 'SUB':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif mnemonic == 'MUL':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
        elif mnemonic == 'DIV':
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            a = stack.pop()
            b = stack.pop()
            if a == 0:
                raise ValueError("Division by zero")
            stack.append(b // a)
        elif mnemonic == 'NEG':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            stack[-1] = -stack[-1]
        elif mnemonic == 'PRINT':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            val = stack.pop()
            output += str(val) + '\n'
        elif mnemonic == 'HALT':
            return output
        elif mnemonic == 'JMP':
            pc = instruction[1]
            pc_increment = 0
        elif mnemonic == 'JZ':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            val = stack.pop()
            if val == 0:
                pc = instruction[1]
                pc_increment = 0
        elif mnemonic == 'JNZ':
            if len(stack) < 1:
                raise ValueError("Stack underflow")
            val = stack.pop()
            if val != 0:
                pc = instruction[1]
                pc_increment = 0
        
        pc += pc_increment
        steps += 1

    return output
