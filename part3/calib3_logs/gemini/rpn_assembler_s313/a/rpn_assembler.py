
import re

def run_asm(src):
    """
    Assembles and runs the RPN assembly code.
    """
    # Pass 1: Build label table
    labels = {}
    program = []
    lines = src.split('\n')
    
    instr_index = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        match = re.match(r'^([a-zA-Z0-9_]+):$', line)
        if match:
            label = match.group(1)
            if label in labels:
                raise ValueError(f"Duplicate label: {label}")
            labels[label] = instr_index
        else:
            instr_index += 1

    # Pass 2: Assemble the program
    for line in lines:
        line = line.split('#', 1)[0].strip()
        if not line or line.endswith(':'):
            continue

        parts = line.split()
        mnemonic = parts[0].upper()
        operands = parts[1:]

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
    output = []
    pc = 0
    
    while pc < len(program):
        instr = program[pc]
        mnemonic = instr[0]

        try:
            if mnemonic == 'PUSH':
                stack.append(instr[1])
                pc += 1
            elif mnemonic == 'POP':
                stack.pop()
                pc += 1
            elif mnemonic == 'DUP':
                stack.append(stack[-1])
                pc += 1
            elif mnemonic == 'SWAP':
                stack[-1], stack[-2] = stack[-2], stack[-1]
                pc += 1
            elif mnemonic == 'ADD':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
                pc += 1
            elif mnemonic == 'SUB':
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
                pc += 1
            elif mnemonic == 'MUL':
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
                pc += 1
            elif mnemonic == 'DIV':
                b = stack.pop()
                a = stack.pop()
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(a // b)
                pc += 1
            elif mnemonic == 'NEG':
                stack[-1] = -stack[-1]
                pc += 1
            elif mnemonic == 'PRINT':
                output.append(str(stack.pop()) + '\n')
                pc += 1
            elif mnemonic == 'HALT':
                break
            elif mnemonic == 'JMP':
                pc = instr[1]
            elif mnemonic == 'JZ':
                val = stack.pop()
                if val == 0:
                    pc = instr[1]
                else:
                    pc += 1
            elif mnemonic == 'JNZ':
                val = stack.pop()
                if val != 0:
                    pc = instr[1]
                else:
                    pc += 1
        except IndexError:
            raise ValueError("Stack underflow")

    return "".join(output)
