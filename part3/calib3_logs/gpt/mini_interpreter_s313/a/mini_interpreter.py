import re

class ParseError(ValueError):
    pass

_token_spec = [
    ('NUMBER', r"\d+"),
    ('NAME', r"[A-Za-z_][A-Za-z0-9_]*"),
    ('OP', r"==|!=|<=|>=|[+\-*/%<>]") ,
    ('LPAREN', r"\("),
    ('RPAREN', r"\)"),
    ('SKIP', r"[ \t]+"),
    ('MISMATCH', r".")
]
_token_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in _token_spec))

class Token:
    def __init__(self, typ, val):
        self.type = typ
        self.val = val
    def __repr__(self):
        return f"Token({self.type},{self.val})"

def tokenize(expr):
    tokens = []
    pos = 0
    while pos < len(expr):
        m = _token_re.match(expr, pos)
        if not m:
            raise ParseError('Unexpected token')
        typ = m.lastgroup
        val = m.group(typ)
        if typ == 'NUMBER':
            tokens.append(Token('NUMBER', int(val)))
        elif typ == 'NAME':
            tokens.append(Token('NAME', val))
        elif typ == 'OP':
            tokens.append(Token('OP', val))
        elif typ == 'LPAREN':
            tokens.append(Token('LPAREN', val))
        elif typ == 'RPAREN':
            tokens.append(Token('RPAREN', val))
        elif typ == 'SKIP':
            pass
        else:
            raise ParseError('Unexpected token')
        pos = m.end()
    tokens.append(Token('EOF', None))
    return tokens

class ExprParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def peek(self):
        return self.tokens[self.pos]
    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok
    def accept_op(self, ops):
        tok = self.peek()
        if tok.type == 'OP' and tok.val in ops:
            self.pos += 1
            return tok.val
        return None
    def expect(self, typ):
        tok = self.peek()
        if tok.type == typ:
            self.pos += 1
            return tok
        raise ParseError('Expected %s' % typ)
    def parse(self):
        node = self.parse_comparison()
        if self.peek().type != 'EOF':
            raise ParseError('Unexpected token')
        return node
    def parse_comparison(self):
        node = self.parse_add()
        while True:
            op = self.accept_op(['==','!=','<','<=','>','>='])
            if not op:
                break
            right = self.parse_add()
            node = ('binop', op, node, right)
        return node
    def parse_add(self):
        node = self.parse_mul()
        while True:
            op = self.accept_op(['+','-'])
            if not op:
                break
            right = self.parse_mul()
            node = ('binop', op, node, right)
        return node
    def parse_mul(self):
        node = self.parse_primary()
        while True:
            op = self.accept_op(['*','/','%'])
            if not op:
                break
            right = self.parse_primary()
            node = ('binop', op, node, right)
        return node
    def parse_primary(self):
        tok = self.peek()
        if tok.type == 'NUMBER':
            self.next()
            return ('num', tok.val)
        if tok.type == 'NAME':
            self.next()
            return ('var', tok.val)
        if tok.type == 'LPAREN':
            self.next()
            node = self.parse_comparison()
            if self.peek().type != 'RPAREN':
                raise ParseError('Unbalanced parentheses')
            self.next()
            return node
        raise ParseError('Unexpected token in expression')

def parse_expression(s):
    try:
        tokens = tokenize(s)
        p = ExprParser(tokens)
        node = p.parse()
        return node
    except ParseError as e:
        raise ValueError('Syntax error')

def eval_expr(node, env):
    t = node[0]
    if t == 'num':
        return node[1]
    if t == 'var':
        name = node[1]
        if name not in env:
            raise ValueError('Undefined variable')
        return env[name]
    if t == 'binop':
        op = node[1]
        lnode = node[2]
        rnode = node[3]
        left = eval_expr(lnode, env)
        right = eval_expr(rnode, env)
        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            if right == 0:
                raise ValueError('Division by zero')
            return left // right
        if op == '%':
            if right == 0:
                raise ValueError('Division by zero')
            return left % right
        if op == '==':
            return 1 if left == right else 0
        if op == '!=':
            return 1 if left != right else 0
        if op == '<':
            return 1 if left < right else 0
        if op == '<=':
            return 1 if left <= right else 0
        if op == '>':
            return 1 if left > right else 0
        if op == '>=':
            return 1 if left >= right else 0
    raise ValueError('Invalid expression')

_name_re = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

def split_lines(src):
    return src.splitlines()

def parse_block(lines, start):
    stmts = []
    i = start
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.strip()
        i += 1
        if line == '' or line.startswith('#'):
            continue
        if line == '}':
            return stmts, i, ''
        if line.startswith('}'):
            # stray text after }
            rem = line[1:].strip()
            return stmts, i, rem
        if line.startswith('if '):
            if not line.endswith('{'):
                raise ValueError('Syntax error')
            cond_str = line[3:-1].strip()
            if cond_str == '':
                raise ValueError('Syntax error')
            cond_expr = parse_expression(cond_str)
            then_stmts, next_i, trailing = parse_block(lines, i)
            i = next_i
            else_stmts = None
            if trailing and trailing.startswith('else'):
                rest = trailing[4:].strip()
                if not rest.startswith('{'):
                    raise ValueError('Syntax error')
                if rest != '{' and rest != '{':
                    pass
                # parse else block
                else_stmts, i2, trailing2 = parse_block(lines, i)
                i = i2
            else:
                # look ahead
                j = i
                while j < n and lines[j].strip() == '':
                    j += 1
                if j < n and lines[j].strip().startswith('else'):
                    el_line = lines[j].strip()
                    if not el_line.endswith('{'):
                        raise ValueError('Syntax error')
                    if el_line != 'else {' and not el_line.startswith('else '):
                        pass
                    j += 1
                    else_stmts, i2, trailing2 = parse_block(lines, j)
                    i = i2
            stmts.append(('if', cond_expr, then_stmts, else_stmts))
            continue
        if line.startswith('while '):
            if not line.endswith('{'):
                raise ValueError('Syntax error')
            cond_str = line[6:-1].strip()
            if cond_str == '':
                raise ValueError('Syntax error')
            cond_expr = parse_expression(cond_str)
            body_stmts, next_i, trailing = parse_block(lines, i)
            if trailing and trailing != '':
                raise ValueError('Syntax error')
            i = next_i
            stmts.append(('while', cond_expr, body_stmts))
            continue
        if line.startswith('print'):
            if not line.startswith('print(') or not line.endswith(')'):
                raise ValueError('Syntax error')
            inner = line[6:-1].strip() if line.startswith('print(') else None
            if inner is None:
                raise ValueError('Syntax error')
            expr = parse_expression(inner)
            stmts.append(('print', expr))
            continue
        # assignment or input
        if '=' in line:
            parts = line.split('=', 1)
            left = parts[0].strip()
            right = parts[1].strip()
            if not _name_re.match(left):
                raise ValueError('Syntax error')
            if right == 'input()':
                stmts.append(('input', left))
                continue
            # else expression
            expr = parse_expression(right)
            stmts.append(('assign', left, expr))
            continue
        raise ValueError('Syntax error')
    # if we reach end without finding closing brace
    raise ValueError('Unbalanced braces')

def parse_program(src):
    lines = split_lines(src)
    stmts, i, trailing = parse_block(lines, 0)
    if i != len(lines):
        # extra content after top-level parsing
        # allow trailing blank lines
        for j in range(i, len(lines)):
            if lines[j].strip() != '':
                raise ValueError('Syntax error')
    return stmts

def exec_block(stmts, env, inputs, out):
    i = 0
    while i < len(stmts):
        st = stmts[i]
        kind = st[0]
        if kind == 'print':
            val = eval_expr(st[1], env)
            out.append(str(val) + '\n')
            i += 1
        elif kind == 'assign':
            name = st[1]
            val = eval_expr(st[2], env)
            env[name] = val
            i += 1
        elif kind == 'input':
            name = st[1]
            if not inputs:
                raise ValueError('No input')
            env[name] = inputs.pop(0)
            i += 1
        elif kind == 'if':
            cond = eval_expr(st[1], env)
            if cond != 0:
                exec_block(st[2], env, inputs, out)
            else:
                if st[3] is not None:
                    exec_block(st[3], env, inputs, out)
            i += 1
        elif kind == 'while':
            cond_expr = st[1]
            body = st[2]
            while True:
                cond = eval_expr(cond_expr, env)
                if cond == 0:
                    break
                exec_block(body, env, inputs, out)
            i += 1
        else:
            raise ValueError('Unknown statement')

def run_program(src, inputs=None):
    if inputs is None:
        inputs = []
    else:
        inputs = list(inputs)
    stmts = parse_program(src)
    env = {}
    out = []
    exec_block(stmts, env, inputs, out)
    return ''.join(out)
