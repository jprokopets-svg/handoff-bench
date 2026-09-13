def run_program(src: str, inputs: list | None = None) -> str:
    if inputs is None:
        inputs = []
    
    # Tokenizer for expressions
    import re
    
    class Token:
        def __init__(self, type, value):
            self.type = type
            self.value = value
        
        def __repr__(self):
            return f"Token({self.type}, {repr(self.value)})"
    
    def tokenize_expr(expr_str):
        # Token types: INT, NAME, OP, COMP, LPAREN, RPAREN
        tokens = []
        i = 0
        expr_str = expr_str.strip()
        while i < len(expr_str):
            ch = expr_str[i]
            if ch.isspace():
                i += 1
                continue
            elif ch.isdigit():
                j = i
                while j < len(expr_str) and expr_str[j].isdigit():
                    j += 1
                tokens.append(Token('INT', int(expr_str[i:j])))
                i = j
            elif ch.isalpha() or ch == '_':
                j = i
                while j < len(expr_str) and (expr_str[j].isalnum() or expr_str[j] == '_'):
                    j += 1
                tokens.append(Token('NAME', expr_str[i:j]))
                i = j
            elif ch in '()':
                tokens.append(Token('LPAREN' if ch == '(' else 'RPAREN', ch))
                i += 1
            elif ch in '*/%+-':
                tokens.append(Token('OP', ch))
                i += 1
            elif ch in '=!<>':
                # Could be =, ==, !=, <, <=, >, >=
                if ch == '=':
                    if i+1 < len(expr_str) and expr_str[i+1] == '=':
                        tokens.append(Token('COMP', '=='))
                        i += 2
                    else:
                        tokens.append(Token('OP', '='))
                        i += 1
                elif ch == '!':
                    if i+1 < len(expr_str) and expr_str[i+1] == '=':
                        tokens.append(Token('COMP', '!='))
                        i += 2
                    else:
                        raise ValueError("Unexpected token '!'")
                elif ch == '<':
                    if i+1 < len(expr_str) and expr_str[i+1] == '=':
                        tokens.append(Token('COMP', '<='))
                        i += 2
                    else:
                        tokens.append(Token('COMP', '<'))
                        i += 1
                elif ch == '>':
                    if i+1 < len(expr_str) and expr_str[i+1] == '=':
                        tokens.append(Token('COMP', '>='))
                        i += 2
                    else:
                        tokens.append(Token('COMP', '>'))
                        i += 1
                else:
                    raise ValueError(f"Unexpected char {ch}")
            else:
                raise ValueError(f"Unexpected character {ch}")
        return tokens
    
    # Parser for expressions using precedence climbing
    class ASTNode:
        pass
    
    class BinOp(ASTNode):
        def __init__(self, left, op, right):
            self.left = left
            self.op = op
            self.right = right
        
        def __repr__(self):
            return f"BinOp({self.left}, {self.op}, {self.right})"
    
    class UnaryOp(ASTNode):
        def __init__(self, op, expr):
            self.op = op
            self.expr = expr
        
        def __repr__(self):
            return f"UnaryOp({self.op}, {self.expr})"
    
    class IntLit(ASTNode):
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"IntLit({self.value})"
    
    class Var(ASTNode):
        def __init__(self, name):
            self.name = name
        
        def __repr__(self):
            return f"Var({self.name})"
    
    def parse_expr(tokens):
        # Precedence levels: 0: comparisons, 1: + -, 2: * / %, 3: primary
        precedence = {
            '==': 0, '!=': 0, '<': 0, '<=': 0, '>': 0, '>=': 0,
            '+': 1, '-': 1,
            '*': 2, '/': 2, '%': 2
        }
        
        def parse_primary():
            nonlocal pos
            if pos >= len(tokens):
                raise ValueError("Unexpected end of expression")
            tok = tokens[pos]
            if tok.type == 'INT':
                pos += 1
                return IntLit(tok.value)
            elif tok.type == 'NAME':
                pos += 1
                return Var(tok.name)
            elif tok.type == 'LPAREN':
                pos += 1
                expr = parse_expr_helper(0)
                if pos >= len(tokens) or tokens[pos].type != 'RPAREN':
                    raise ValueError("Missing closing parenthesis")
                pos += 1
                return expr
            else:
                raise ValueError(f"Unexpected token {tok.type} in expression")
        
        def parse_expr_helper(min_prec):
            nonlocal pos
            left = parse_primary()
            
            while pos < len(tokens):
                tok = tokens[pos]
                if tok.type == 'OP' and tok.value in precedence:
                    op = tok.value
                    prec = precedence[op]
                    if prec < min_prec:
                        break
                    pos += 1
                    right = parse_expr_helper(prec + 1)
                    left = BinOp(left, op, right)
                elif tok.type == 'COMP':
                    op = tok.value
                    prec = precedence[op]
                    if prec < min_prec:
                        break
                    pos += 1
                    right = parse_expr_helper(prec + 1)
                    left = BinOp(left, op, right)
                else:
                    break
            return left
        
        pos = 0
        result = parse_expr_helper(0)
        if pos != len(tokens):
            raise ValueError("Trailing tokens in expression")
        return result
    
    # Evaluator
    def evaluate(node, env):
        if isinstance(node, IntLit):
            return node.value
        elif isinstance(node, Var):
            if node.name not in env:
                raise ValueError(f"Undefined variable {node.name}")
            return env[node.name]
        elif isinstance(node, BinOp):
            left_val = evaluate(node.left, env)
            right_val = evaluate(node.right, env)
            op = node.op
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                if right_val == 0:
                    raise ValueError("Division by zero")
                return left_val // right_val  # integer division
            elif op == '%':
                if right_val == 0:
                    raise ValueError("Modulo by zero")
                return left_val % right_val
            elif op == '==':
                return 1 if left_val == right_val else 0
            elif op == '!=':
                return 1 if left_val != right_val else 0
            elif op == '<':
                return 1 if left_val < right_val else 0
            elif op == '<=':
                return 1 if left_val <= right_val else 0
            elif op == '>':
                return 1 if left_val > right_val else 0
            elif op == '>=':
                return 1 if left_val >= right_val else 0
            else:
                raise ValueError(f"Unknown operator {op}")
        else:
            raise ValueError(f"Unknown AST node {type(node)}")
    
    # Statement parser and executor
    class Statement:
        pass
    
    class Assign(Statement):
        def __init__(self, var, expr):
            self.var = var
            self.expr = expr
        
        def execute(self, env, inputs, output):
            env[self.var] = evaluate(self.expr, env)
    
    class InputAssign(Statement):
        def __init__(self, var):
            self.var = var
        
        def execute(self, env, inputs, output):
            if not inputs:
                raise ValueError("No more inputs")
            env[self.var] = inputs.pop(0)
    
    class Print(Statement):
        def __init__(self, expr):
            self.expr = expr
        
        def execute(self, env, inputs, output):
            val = evaluate(self.expr, env)
            output.append(str(val))
    
    class If(Statement):
        def __init__(self, cond, then_block, else_block):
            self.cond = cond
            self.then_block = then_block
            self.else_block = else_block
        
        def execute(self, env, inputs, output):
            cond_val = evaluate(self.cond, env)
            if cond_val != 0:
                for stmt in self.then_block:
                    stmt.execute(env, inputs, output)
            elif self.else_block:
                for stmt in self.else_block:
                    stmt.execute(env, inputs, output)
    
    class While(Statement):
        def __init__(self, cond, body):
            self.cond = cond
            self.body = body
        
        def execute(self, env, inputs, output):
            while evaluate(self.cond, env) != 0:
                for stmt in self.body:
                    stmt.execute(env, inputs, output)
    
    def parse_statement(line, lines, line_idx):
        line = line.strip()
        if not line:
            return None, line_idx
        
        # Check for block end
        if line == '}':
            return 'BLOCK_END', line_idx
        
        # Check for if statement
        if line.startswith('if '):
            # Parse condition up to {
            if not line.endswith('{'):
                raise ValueError("Missing '{' after if condition")
            cond_str = line[3:-1].strip()
            cond_tokens = tokenize_expr(cond_str)
            cond_expr = parse_expr(cond_tokens)
            
            # Parse then block
            then_block = []
            line_idx += 1
            while line_idx < len(lines):
                stmt, line_idx = parse_statement(lines[line_idx], lines, line_idx)
                if stmt == 'BLOCK_END':
                    break
                if stmt is not None:
                    then_block.append(stmt)
            
            # Check for else
            else_block = None
            if line_idx < len(lines):
                next_line = lines[line_idx].strip()
                if next_line == 'else {':
                    line_idx += 1
                    else_block = []
                    while line_idx < len(lines):
                        stmt, line_idx = parse_statement(lines[line_idx], lines, line_idx)
                        if stmt == 'BLOCK_END':
                            break
                        if stmt is not None:
                            else_block.append(stmt)
                elif next_line.startswith('} else {'):
                    # Handle } else { on same line
                    line_idx += 1
                    else_block = []
                    while line_idx < len(lines):
                        stmt, line_idx = parse_statement(lines[line_idx], lines, line_idx)
                        if stmt == 'BLOCK_END':
                            break
                        if stmt is not None:
                            else_block.append(stmt)
            
            return If(cond_expr, then_block, else_block), line_idx
        
        # Check for while statement
        if line.startswith('while '):
            if not line.endswith('{'):
                raise ValueError("Missing '{' after while condition")
            cond_str = line[6:-1].strip()
            cond_tokens = tokenize_expr(cond_str)
            cond_expr = parse_expr(cond_tokens)
            
            # Parse body
            body = []
            line_idx += 1
            while line_idx < len(lines):
                stmt, line_idx = parse_statement(lines[line_idx], lines, line_idx)
                if stmt == 'BLOCK_END':
                    break
                if stmt is not None:
                    body.append(stmt)
            
            return While(cond_expr, body), line_idx
        
        # Check for print
        if line.startswith('print(') and line.endswith(')'):
            expr_str = line[6:-1].strip()
            expr_tokens = tokenize_expr(expr_str)
            expr_ast = parse_expr(expr_tokens)
            return Print(expr_ast), line_idx
        
        # Check for assignment
        if '=' in line:
            parts = line.split('=', 1)
            var = parts[0].strip()
            expr_str = parts[1].strip()
            
            # Check for input()
            if expr_str == 'input()':
                return InputAssign(var), line_idx
            
            # Regular assignment
            expr_tokens = tokenize_expr(expr_str)
            expr_ast = parse_expr(expr_tokens)
            return Assign(var, expr_ast), line_idx
        
        raise ValueError(f"Syntax error: {line}")
    
    # Main execution
    lines = src.splitlines()
    # Remove empty lines and strip whitespace
    lines = [line.rstrip('\n') for line in lines]
    
    env = {}
    output = []
    inputs = list(inputs)  # Make a copy to pop from
    
    line_idx = 0
    while line_idx < len(lines):
        stmt, line_idx = parse_statement(lines[line_idx], lines, line_idx)
        if stmt is not None and stmt != 'BLOCK_END':
            stmt.execute(env, inputs, output)
        line_idx += 1
    
    return '\n'.join(output) + ('\n' if output else '')