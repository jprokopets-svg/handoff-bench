import re
from typing import List, Tuple, Optional


def run_asm(src: str) -> str:
    # Parse and assemble
    lines = src.splitlines()
    instrs: List[Tuple[str, Optional[object]]] = []  # (mnemonic, arg)
    labels = {}
    label_re = re.compile(r'^[A-Za-z0-9_]+$')

    for raw in lines:
        # remove comments
        line = raw
        if '#' in line:
            line = line[: line.index('#')]
        line = line.strip()
        if not line:
            continue
        # label line
        if line.endswith(':'):
            name = line[:-1].strip()
            if not name or not label_re.match(name):
                raise ValueError(f'invalid label: {name}')
            if name in labels:
                raise ValueError('duplicate label')
            labels[name] = len(instrs)
            continue
        parts = line.split()
        if not parts:
            continue
        op = parts[0].upper()
        args = parts[1:]
        # validate operand counts
        if op == 'PUSH':
            if len(args) != 1:
                raise ValueError('wrong operand count')
            try:
                val = int(args[0])
            except Exception:
                raise ValueError('non-integer PUSH')
            instrs.append((op, val))
        elif op in ('JMP', 'JZ', 'JNZ'):
            if len(args) != 1:
                raise ValueError('wrong operand count')
            name = args[0]
            if not label_re.match(name):
                raise ValueError('invalid label')
            instrs.append((op, name))
        elif op in ('POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 'NEG', 'PRINT', 'HALT'):
            if len(args) != 0:
                raise ValueError('wrong operand count')
            instrs.append((op, None))
        else:
            raise ValueError('unknown mnemonic')

    # resolve labels for jumps
    resolved: List[Tuple[str, Optional[object]]] = []
    for op, arg in instrs:
        if op in ('JMP', 'JZ', 'JNZ'):
            name = arg
            if name not in labels:
                raise ValueError('undefined label')
            resolved.append((op, labels[name]))
        else:
            resolved.append((op, arg))

    # execute
    stack: List[int] = []
    out_lines: List[str] = []
    ip = 0
    n = len(resolved)
    while ip < n:
        op, arg = resolved[ip]
        if op == 'PUSH':
            stack.append(arg)  # type: ignore
            ip += 1
        elif op == 'POP':
            if not stack:
                raise ValueError('stack underflow')
            stack.pop()
            ip += 1
        elif op == 'DUP':
            if not stack:
                raise ValueError('stack underflow')
            stack.append(stack[-1])
            ip += 1
        elif op == 'SWAP':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
            ip += 1
        elif op == 'ADD':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
            ip += 1
        elif op == 'SUB':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
            ip += 1
        elif op == 'MUL':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
            ip += 1
        elif op == 'DIV':
            if len(stack) < 2:
                raise ValueError('stack underflow')
            a = stack.pop()
            b = stack.pop()
            if a == 0:
                raise ValueError('division by zero')
            # integer division truncated toward zero
            stack.append(int(b / a))
            ip += 1
        elif op == 'NEG':
            if not stack:
                raise ValueError('stack underflow')
            stack[-1] = -stack[-1]
            ip += 1
        elif op == 'PRINT':
            if not stack:
                raise ValueError('stack underflow')
            v = stack.pop()
            out_lines.append(str(v) + '\n')
            ip += 1
        elif op == 'HALT':
            break
        elif op == 'JMP':
            ip = arg  # type: ignore
        elif op == 'JZ':
            if not stack:
                raise ValueError('stack underflow')
            v = stack.pop()
            if v == 0:
                ip = arg  # type: ignore
            else:
                ip += 1
        elif op == 'JNZ':
            if not stack:
                raise ValueError('stack underflow')
            v = stack.pop()
            if v != 0:
                ip = arg  # type: ignore
            else:
                ip += 1
        else:
            raise ValueError('unknown mnemonic')

    return ''.join(out_lines)
