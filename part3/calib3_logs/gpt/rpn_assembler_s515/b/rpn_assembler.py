import re
from typing import List, Tuple, Optional


def run_asm(src: str) -> str:
    # Parse source lines: strip comments (# to end of line), strip whitespace, skip blanks
    raw_lines = src.splitlines()
    lines: List[Tuple[int, str]] = []  # (original line number starting at 1, content)
    for i, raw in enumerate(raw_lines, start=1):
        # remove comment
        idx = raw.find('#')
        if idx != -1:
            raw = raw[:idx]
        raw = raw.strip()
        if raw == '':
            continue
        lines.append((i, raw))

    # First pass: collect labels and instructions
    labels = {}  # name -> instruction index
    instructions: List[Tuple[str, Optional[str], int]] = []  # (mnemonic, operand, src_line)

    label_re = re.compile(r'^[A-Za-z0-9_]+$')

    for ln, content in lines:
        if content.endswith(':'):
            name = content[:-1].strip()
            if not name or not label_re.match(name):
                raise ValueError(f"invalid label '{name}'")
            if name in labels:
                raise ValueError(f"duplicate label '{name}'")
            labels[name] = len(instructions)
        else:
            parts = content.split()
            mnemonic = parts[0]
            operand = None
            if len(parts) > 1:
                operand = ' '.join(parts[1:])
            instructions.append((mnemonic, operand, ln))

    # Validate mnemonics and operands; for jumps keep label name to resolve later
    VALID_ZERO = {'POP', 'DUP', 'SWAP', 'ADD', 'SUB', 'MUL', 'DIV', 'NEG', 'PRINT', 'HALT'}
    VALID_ONE_LABEL = {'JMP', 'JZ', 'JNZ'}
    all_mnemonics = VALID_ZERO.union(VALID_ONE_LABEL).union({'PUSH'})

    # We'll store resolved operands: for PUSH store int, for jumps store target index
    resolved: List[Tuple[str, Optional[object], int]] = []

    for mnemonic, operand, ln in instructions:
        if mnemonic not in all_mnemonics:
            raise ValueError(f"unknown mnemonic '{mnemonic}'")
        if mnemonic == 'PUSH':
            if operand is None:
                raise ValueError('PUSH requires an integer operand')
            # operand should be an integer literal (can be negative)
            try:
                val = int(operand)
            except Exception:
                raise ValueError('PUSH requires an integer operand')
            resolved.append((mnemonic, val, ln))
        elif mnemonic in VALID_ZERO:
            if operand is not None:
                raise ValueError(f"wrong operand count for {mnemonic}")
            resolved.append((mnemonic, None, ln))
        elif mnemonic in VALID_ONE_LABEL:
            if operand is None:
                raise ValueError(f"{mnemonic} requires a label operand")
            # leave as label name for now; will resolve after checking existence
            if not label_re.match(operand):
                # invalid label name
                raise ValueError(f"invalid label '{operand}'")
            resolved.append((mnemonic, operand, ln))
        else:
            # shouldn't happen
            raise ValueError(f"unknown mnemonic '{mnemonic}'")

    # Resolve jump labels
    for i, (mnemonic, operand, ln) in enumerate(resolved):
        if mnemonic in VALID_ONE_LABEL:
            label_name = operand  # type: ignore
            if label_name not in labels:
                raise ValueError(f"undefined label '{label_name}'")
            target = labels[label_name]
            resolved[i] = (mnemonic, target, ln)

    # Execution
    stack: List[int] = []
    output_parts: List[str] = []
    ip = 0
    n = len(resolved)

    def need(nneed: int):
        if len(stack) < nneed:
            raise ValueError('stack underflow')

    while ip < n:
        mnemonic, operand, ln = resolved[ip]
        # default next ip
        next_ip = ip + 1
        if mnemonic == 'PUSH':
            stack.append(operand)  # type: ignore
        elif mnemonic == 'POP':
            need(1)
            stack.pop()
        elif mnemonic == 'DUP':
            need(1)
            stack.append(stack[-1])
        elif mnemonic == 'SWAP':
            need(2)
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
        elif mnemonic == 'ADD':
            need(2)
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
        elif mnemonic == 'SUB':
            need(2)
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif mnemonic == 'MUL':
            need(2)
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
        elif mnemonic == 'DIV':
            need(2)
            a = stack.pop()
            b = stack.pop()
            if a == 0:
                raise ValueError('division by zero')
            stack.append(b // a)
        elif mnemonic == 'NEG':
            need(1)
            a = stack.pop()
            stack.append(-a)
        elif mnemonic == 'PRINT':
            need(1)
            a = stack.pop()
            output_parts.append(f"{a}\n")
        elif mnemonic == 'HALT':
            break
        elif mnemonic == 'JMP':
            target = operand  # type: ignore
            if target == n:
                break
            next_ip = target
        elif mnemonic == 'JZ':
            need(1)
            a = stack.pop()
            if a == 0:
                target = operand  # type: ignore
                if target == n:
                    break
                next_ip = target
        elif mnemonic == 'JNZ':
            need(1)
            a = stack.pop()
            if a != 0:
                target = operand  # type: ignore
                if target == n:
                    break
                next_ip = target
        else:
            raise ValueError(f"unknown mnemonic '{mnemonic}'")

        ip = next_ip

    return ''.join(output_parts)
