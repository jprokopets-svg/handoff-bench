
import re

def run_asm(src: str) -> str:
    # Pass 1: Find labels and clean lines
    labels = {}
    program_lines = []
    lines = src.splitlines()

    for line_num, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if '#' in line:
            line = line[:line.find('#')].strip()
        
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

    # Pass 2: Assemble the program
    instructions = []
    for line in program_lines:
        parts = line.split()
        mnemonic = parts[0].upper()
        operands = parts[1:]

        if mnemonic == 'PUSH':
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for PUSH")
            try:
                instructions.append(('PUSH', int(operands[0])))
            except ValueError:
                raise ValueError(f"Non-integer operand for PUSH: {operands[0]}")
        elif mnemonic in ['POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 'NEG', 'PRINT', 'HALT']:
            if len(operands) != 0:
                raise ValueError(f"Wrong operand count for {mnemonic}")
            instructions.append((mnemonic,))
        elif mnemonic in ['JMP', 'JZ', 'JNZ']:
            if len(operands) != 1:
                raise ValueError(f"Wrong operand count for {mnemonic}")
            label = operands[0]
            if label not in labels:
                raise ValueError(f"Undefined label: {label}")
            instructions.append((mnemonic, labels[label]))
        else:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")

    # --- Execution ---
    stack = []
    output = ""
    pc = 0
    while 0 <= pc < len(instructions):
        instr = instructions[pc]
        mnemonic = instr[0]
        pc_updated = False

        if mnemonic == 'PUSH':
            stack.append(instr[1])
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
        elif mnemonic in ['ADD', 'SUB', 'MUL', 'DIV']:
            if len(stack) < 2:
                raise ValueError("Stack underflow")
            op2 = stack.pop()
            op1 = stack.pop()
            if mnemonic == 'ADD':
                stack.append(op1 + op2)
            elif mnemonic == 'SUB':
                stack.append(op1 - op2)
            elif mnemonic == 'MUL':
                stack.append(op1 * op2)
            elif mnemonic == 'DIV':
                if op2 == 0:
                    raise ValueError("Division by zero")
                stack.append(op1 // op2)
        elif mnemonic == 'NEG':
            if not stack:
                raise ValueError("Stack underflow")
            stack[-1] = -stack[-1]
        elif mnemonic == 'PRINT':
            if not stack:
                raise ValueError("Stack underflow")
            output += str(stack.pop()) + '\n'
        elif mnemonic == 'HALT':
            break
        elif mnemonic == 'JMP':
            pc = instr[1]
            pc_updated = True
        elif mnemonic == 'JZ':
            if not stack:
                raise ValueError("Stack underflow")
            val = stack.pop()
            if val == 0:
                pc = instr[1]
                pc_updated = True
        elif mnemonic == 'JNZ':
            if not stack:
                raise ValueError("Stack underflow")
            val = stack.pop()
            if val != 0:
                pc = instr[1]
                pc_updated = True
        
        if not pc_updated:
            pc += 1

    return output
