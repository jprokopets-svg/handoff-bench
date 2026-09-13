import re


class Instruction:
    def __init__(self, op, arg=None, src_line=None):
        self.op = op
        self.arg = arg
        self.src_line = src_line


def run_asm(src: str) -> str:
    lines = src.splitlines()
    # First pass: parse lines, collect labels and instructions
    labels = {}
    instrs = []
    line_no = 0
    for raw in lines:
        line_no += 1
        # strip comments
        if '#' in raw:
            raw = raw.split('#', 1)[0]
        s = raw.strip()
        if not s:
            continue
        # label?
        if s.endswith(':'):
            name = s[:-1].strip()
            # name must be alphanumeric + underscore
            if not name or not re.fullmatch(r"[A-Za-z0-9_]+", name):
                raise ValueError(f"invalid label name: {name}")
            if name in labels:
                raise ValueError("duplicate label")
            labels[name] = len(instrs)
            continue
        # instruction
        parts = s.split()
        op = parts[0]
        args = parts[1:]
        instrs.append(Instruction(op, args, src_line=line_no))

    # Validate mnemonics and operand counts and resolve PUSH int
    valid_noarg = {"POP", "DUP", "SWAP", "ADD", "SUB", "MUL", "DIV", "NEG", "PRINT", "HALT"}
    valid_onearg = {"PUSH", "JMP", "JZ", "JNZ"}
    for ins in instrs:
        op = ins.op
        args = ins.arg
        if op in valid_noarg:
            if args:
                raise ValueError("wrong operand count")
        elif op in valid_onearg:
            if len(args) != 1:
                raise ValueError("wrong operand count")
            if op == 'PUSH':
                # parse integer
                try:
                    v = int(args[0])
                except Exception:
                    raise ValueError("non-integer PUSH")
                ins.arg = v
            else:
                # jump label; keep as string for now
                ins.arg = args[0]
                if not re.fullmatch(r"[A-Za-z0-9_]+", ins.arg):
                    # label name invalid format
                    raise ValueError("undefined label")
        else:
            raise ValueError("unknown mnemonic")

    # Resolve labels used in jumps
    for ins in instrs:
        if ins.op in ('JMP', 'JZ', 'JNZ'):
            label = ins.arg
            if label not in labels:
                raise ValueError("undefined label")
            ins.arg = labels[label]

    # Execute
    output_parts = []
    stack = []
    pc = 0
    n = len(instrs)
    while pc < n:
        ins = instrs[pc]
        op = ins.op
        # default next
        next_pc = pc + 1
        if op == 'PUSH':
            stack.append(ins.arg)
        elif op == 'POP':
            if not stack:
                raise ValueError("stack underflow")
            stack.pop()
        elif op == 'DUP':
            if not stack:
                raise ValueError("stack underflow")
            stack.append(stack[-1])
        elif op == 'SWAP':
            if len(stack) < 2:
                raise ValueError("stack underflow")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif op in ('ADD', 'SUB', 'MUL', 'DIV'):
            if len(stack) < 2:
                raise ValueError("stack underflow")
            a = stack.pop()
            b = stack.pop()
            if op == 'ADD':
                stack.append(b + a)
            elif op == 'SUB':
                stack.append(b - a)
            elif op == 'MUL':
                stack.append(b * a)
            else:  # DIV
                if a == 0:
                    raise ValueError("division by zero")
                stack.append(b // a)
        elif op == 'NEG':
            if not stack:
                raise ValueError("stack underflow")
            stack[-1] = -stack[-1]
        elif op == 'PRINT':
            if not stack:
                raise ValueError("stack underflow")
            v = stack.pop()
            output_parts.append(str(v) + '\n')
        elif op == 'HALT':
            break
        elif op == 'JMP':
            # set pc to arg
            next_pc = ins.arg
        elif op == 'JZ':
            if not stack:
                raise ValueError("stack underflow")
            v = stack.pop()
            if v == 0:
                next_pc = ins.arg
        elif op == 'JNZ':
            if not stack:
                raise ValueError("stack underflow")
            v = stack.pop()
            if v != 0:
                next_pc = ins.arg
        else:
            raise ValueError("unknown mnemonic")

        pc = next_pc
    return ''.join(output_parts)
