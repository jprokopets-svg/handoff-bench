from typing import List, Tuple, Optional


class ParseError(Exception):
    pass


def run_program(src: str, inputs: list | None = None) -> str:
    try:
        parser = Parser(src)
        prog = parser.parse_program()
        executor = Executor(prog, inputs or [])
        return executor.execute()
    except ValueError:
        raise
    except Exception as e:
        # convert any internal parse/execution errors to ValueError as required
        raise ValueError from e


# Parser and AST

class Parser:
    def __init__(self, src: str):
        self.lines = src.splitlines()
        self.n = len(self.lines)

    def parse_program(self):
        stmts, next_i = self._parse_block(0, allow_end=True)
        if next_i != self.n:
            # stray closing brace or extra lines
            # if remaining lines are blank, ok
            for i in range(next_i, self.n):
                if self.lines[i].strip() != '':
                    raise ParseError('trailing')
        return stmts

    def _parse_block(self, i: int, allow_end: bool = False) -> Tuple[List, int]:
        stmts = []
        while i < self.n:
            line = self.lines[i].strip()
            if line == '':
                i += 1
                continue
            if line == '}':
                return stmts, i + 1
            # if this line ends with '{' it's a block opener
            if line.startswith('if ' ) and line.endswith('{'):
                cond_s = line[3:-1].strip()
                cond = cond_s
                # parse inner block
                inner, ni = self._parse_block(i + 1)
                # check for else
                else_block = None
                if ni < self.n:
                    nextline = self.lines[ni].strip()
                    if nextline == 'else {':
                        else_block, ni2 = self._parse_block(ni + 1)
                        ni = ni2
                stmts.append(('if', cond, inner, else_block))
                i = ni
                continue
            if line.startswith('while ') and line.endswith('{'):
                cond_s = line[6:-1].strip()
                inner, ni = self._parse_block(i + 1)
                stmts.append(('while', cond_s, inner))
                i = ni
                continue
            # assignment or print
            if line.startswith('print(') and line.endswith(')'):
                expr = line[len('print('):-1].strip()
                if expr == '':
                    raise ParseError('empty print')
                stmts.append(('print', expr))
                i += 1
                continue
            # assignment
            if '=' in line:
                parts = line.split('=')
                if len(parts) < 2:
                    raise ParseError('bad assign')
                lhs = parts[0].strip()
                rhs = '='.join(parts[1:]).strip()
                if lhs == '' or not lhs.isidentifier():
                    raise ParseError('bad lhs')
                if rhs == 'input()':
                    stmts.append(('input', lhs))
                else:
                    stmts.append(('assign', lhs, rhs))
                i += 1
                continue
            # stray closing brace
            if line == '}':
                return stmts, i + 1
            # unknown
            raise ParseError('syntax')
        if not allow_end:
            # if we were parsing a block but hit EOF without closing
            # But top-level parse allows EOF
            return stmts, self.n
        return stmts, self.n


# Simple expression evaluator using shunting-yard to RPN

class ExprEval:
    def __init__(self, expr: str):
        self.expr = expr
        self.tokens = self.tokenize(expr)
        if not self.tokens:
            raise ParseError('empty expr')
        self.rpn = self.to_rpn(self.tokens)

    def tokenize(self, s: str):
        tokens = []
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            if c.isspace():
                i += 1
                continue
            if c.isdigit():
                j = i
                while j < n and s[j].isdigit():
                    j += 1
                tokens.append(('num', int(s[i:j])))
                i = j
                continue
            if c.isalpha() or c == '_':
                j = i
                while j < n and (s[j].isalnum() or s[j] == '_'):
                    j += 1
                tokens.append(('name', s[i:j]))
                i = j
                continue
            # multi-char operators
            if s.startswith('==', i) or s.startswith('!=', i) or s.startswith('<=', i) or s.startswith('>=', i):
                tokens.append(('op', s[i:i+2]))
                i += 2
                continue
            if c in '+-*/%()<>' :
                tokens.append(('op', c))
                i += 1
                continue
            raise ParseError('bad char')
        return tokens

    def to_rpn(self, tokens):
        prec = {
            '==': 1, '!=': 1, '<': 1, '<=': 1, '>': 1, '>=': 1,
            '+': 2, '-': 2,
            '*': 3, '/': 3, '%': 3,
        }
        output = []
        stack = []
        for ttype, val in tokens:
            if ttype == 'num' or ttype == 'name':
                output.append((ttype, val))
            else:
                # operator or paren
                if val == '(':
                    stack.append(val)
                elif val == ')':
                    while stack and stack[-1] != '(':
                        output.append(('op', stack.pop()))
                    if not stack or stack[-1] != '(':
                        raise ParseError('mismatched paren')
                    stack.pop()
                else:
                    # operator
                    while stack and stack[-1] != '(' and prec.get(stack[-1], 0) >= prec.get(val, 0):
                        output.append(('op', stack.pop()))
                    stack.append(val)
        while stack:
            v = stack.pop()
            if v in '()':
                raise ParseError('mismatched paren')
            output.append(('op', v))
        return output

    def eval(self, env: dict):
        st = []
        for ttype, val in self.rpn:
            if ttype == 'num':
                st.append(val)
            elif ttype == 'name':
                if val == 'input':
                    # input should be used as input() only
                    raise ParseError('bad input')
                if val not in env:
                    raise ValueError('undef')
                st.append(env[val])
            else:
                if val in ('+', '-', '*', '/', '%', '==', '!=', '<', '<=', '>', '>='):
                    if len(st) < 2:
                        raise ParseError('trailing op')
                    b = st.pop()
                    a = st.pop()
                    if val == '+':
                        st.append(a + b)
                    elif val == '-':
                        st.append(a - b)
                    elif val == '*':
                        st.append(a * b)
                    elif val == '/':
                        if b == 0:
                            raise ValueError('div0')
                        st.append(a // b)
                    elif val == '%':
                        if b == 0:
                            raise ValueError('mod0')
                        st.append(a % b)
                    elif val == '==':
                        st.append(1 if a == b else 0)
                    elif val == '!=':
                        st.append(1 if a != b else 0)
                    elif val == '<':
                        st.append(1 if a < b else 0)
                    elif val == '<=':
                        st.append(1 if a <= b else 0)
                    elif val == '>':
                        st.append(1 if a > b else 0)
                    elif val == '>=':
                        st.append(1 if a >= b else 0)
                else:
                    raise ParseError('bad op')
        if len(st) != 1:
            raise ParseError('bad expr')
        return st[0]


class Executor:
    def __init__(self, stmts, inputs: list):
        self.stmts = stmts
        self.env = {}
        self.inputs = list(inputs)
        self.out_lines = []

    def execute(self):
        self._exec_block(self.stmts)
        return ''.join(line + '\n' for line in self.out_lines)

    def _eval_expr(self, expr: str) -> int:
        ee = ExprEval(expr)
        return ee.eval(self.env)

    def _exec_block(self, stmts):
        i = 0
        while i < len(stmts):
            s = stmts[i]
            typ = s[0]
            if typ == 'print':
                val = self._eval_expr(s[1])
                self.out_lines.append(str(val))
            elif typ == 'assign':
                v = self._eval_expr(s[2])
                self.env[s[1]] = v
            elif typ == 'input':
                if not self.inputs:
                    raise ValueError('no input')
                self.env[s[1]] = self.inputs.pop(0)
            elif typ == 'if':
                cond = self._eval_expr(s[1])
                if cond != 0:
                    self._exec_block(s[2])
                else:
                    if s[3] is not None:
                        self._exec_block(s[3])
            elif typ == 'while':
                while self._eval_expr(s[1]) != 0:
                    self._exec_block(s[2])
            else:
                raise ParseError('bad stmt')
            i += 1
