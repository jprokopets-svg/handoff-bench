import re

LABEL_RE = re.compile(r'^[A-Za-z0-9_]+$')


def run_asm(src: str) -> str:
    # Parse and assemble
    lines = src.splitlines()
    instructions = []  # each instruction: tuple (mnemonic, operand) where operand may be int or label name
    labels = {}

    for raw in lines:
        # remove comment
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        # label
        if line.endswith(':'):
            name = line[:-1].strip()
            if not name or not LABEL_RE.match(name):
                raise ValueError('invalid label name')
            if name in labels:
                raise ValueError('duplicate label')
            labels[name] = len(instructions)
            continue
        parts = line.split()
        mnemonic = parts[0]
        # validate mnemonics
        if mnemonic == 'PUSH':
            if len(parts) != 2:
                raise ValueError('PUSH requires one operand')
            arg = parts[1]
            try:
                val = int(arg)
            except Exception:
                raise ValueError('PUSH operand must be integer')
            instructions.append(('PUSH', val))
        elif mnemonic in ('JMP', 'JZ', 'JNZ'):
            if len(parts) != 2:
                raise ValueError(f'{mnemonic} requires one operand')
            name = parts[1]
            if not LABEL_RE.match(name):
                raise ValueError('invalid label name')
            instructions.append((mnemonic, name))
        elif mnemonic in ('POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 'NEG', 'PRINT', 'HALT'):
            if len(parts) != 1:
                raise ValueError(f'{mnemonic} takes no operands')
            instructions.append((mnemonic, None))
        else:
            raise ValueError('unknown mnemonic')

    # Resolve labels for jump operands
    for i, (mnemonic, operand) in enumerate(instructions):
        if mnemonic in ('JMP', 'JZ', 'JNZ'):
            label = operand
            if label not in labels:
                raise ValueError('undefined label')
            # replace with target index
            instructions[i] = (mnemonic, labels[label])

    # Execute
    stack = []
    output_parts = []
    ip = 0
    L = len(instructions)
    while ip < L:
        instr, operand = instructions[ip]
        # default increment
        next_ip = ip + 1
        if instr == 'PUSH':
            stack.append(operand)
        elif instr == 'POP':
            if not stack:
                raise ValueError('stack underflow')
            stack.pop()
        elif instr == 'DUP':
            if not stack:
                raise ValueError('stack underflow')
            stack.append(stack[-1])
        elif instr == 'SWAP':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif instr == 'ADD':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
        elif instr == 'SUB':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif instr == 'MUL':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
        elif instr == 'DIV':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            if a == 0:
                raise ValueError('division by zero')
            stack.append(b // a)
        elif instr == 'NEG':
            if not stack:
                raise ValueError('stack underflow')
            stack[-1] = -stack[-1]
        elif instr == 'PRINT':
            if not stack:
                raise ValueError('stack underflow')
            v = stack.pop()
            output_parts.append(str(v) + '\n')
        elif instr == 'HALT':
            break
        elif instr == 'JMP':
            next_ip = operand
        elif instr == 'JZ':
            if not stack:
                raise ValueError('stack underflow')
            v = stack.pop()
            if v == 0:
                next_ip = operand
        elif instr == 'JNZ':
            if not stack:
                raise ValueError('stack underflow')
            v = stack.pop()
            if v != 0:
                next_ip = operand
        else:
            raise ValueError('unknown instruction')

        ip = next_ip
    return ''.join(output_parts)
