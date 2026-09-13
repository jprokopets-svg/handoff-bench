
import re

def run_asm(src):
    lines = src.split('\n')
    
    # 1st Pass: Parse and find labels
    instructions = []
    labels = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Strip comments
        if '#' in line:
            line = line[:line.find('#')].strip()

        if line.endswith(':'):
            label = line[:-1]
            if not re.match(r'^[a-zA-Z0-9_]+$', label):
                raise ValueError(f"Invalid label name: {label}")
            if label in labels:
                raise ValueError(f"Duplicate label: {label}")
            labels[label] = len(instructions)
            continue

        parts = line.split()
        instructions.append(parts)

    # 2nd Pass: Assemble instructions
    program = []
    for instruction in instructions:
        mnemonic = instruction[0].upper()
        operands = instruction[1:]

        if mnemonic == 'PUSH':
            if len(operands) != 1:
                raise ValueError("PUSH requires one operand")
            try:
                val = int(operands[0])
                program.append(('PUSH', val))
            except ValueError:
                raise ValueError("PUSH operand must be an integer")
        elif mnemonic in ['POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 'NEG', 'PRINT', 'HALT']:
            if len(operands) != 0:
                raise ValueError(f"{mnemonic} takes no operands")
            program.append((mnemonic,))
        elif mnemonic in ['JMP', 'JZ', 'JNZ']:
            if len(operands) != 1:
                raise ValueError(f"{mnemonic} requires one operand")
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            program.append((mnemonic, labels[label]))
        else:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")

    # Simulation
    stack = []
    pc = 0
    output = ""
    
    while pc < len(program):
        instruction = program[pc]
        op = instruction[0]
        
        pc += 1

        if op == 'PUSH':
            stack.append(instruction[1])
        elif op == 'POP':
            if len(stack) < 1: raise ValueError("Stack underflow")
            stack.pop()
        elif op == 'DUP':
            if len(stack) < 1: raise ValueError("Stack underflow")
            stack.append(stack[-1])
        elif op == 'SWAP':
            if len(stack) < 2: raise ValueError("Stack underflow")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif op == 'ADD':
            if len(stack) < 2: raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif op == 'SUB':
            if len(stack) < 2: raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif op == 'MUL':
            if len(stack) < 2: raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif op == 'DIV':
            if len(stack) < 2: raise ValueError("Stack underflow")
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ValueError("Division by zero")
            stack.append(a // b)
        elif op == 'NEG':
            if len(stack) < 1: raise ValueError("Stack underflow")
            stack[-1] = -stack[-1]
        elif op == 'PRINT':
            if len(stack) < 1: raise ValueError("Stack underflow")
            output += str(stack.pop()) + '\n'
        elif op == 'HALT':
            return output
        elif op == 'JMP':
            pc = instruction[1]
        elif op == 'JZ':
            if len(stack) < 1: raise ValueError("Stack underflow")
            val = stack.pop()
            if val == 0:
                pc = instruction[1]
        elif op == 'JNZ':
            if len(stack) < 1: raise ValueError("Stack underflow")
            val = stack.pop()
            if val != 0:
                pc = instruction[1]

    return output
