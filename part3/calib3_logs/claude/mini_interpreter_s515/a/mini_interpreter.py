def run_program(src: str, inputs: list | None = None) -> str:
    """Execute a tiny imperative programming language."""
    if inputs is None:
        inputs = []
    
    lines = src.split('\n')
    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    
    variables = {}
    output = []
    input_index = [0]  # Use list to allow modification in nested functions
    
    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.pos = 0
        
        def peek(self):
            if self.pos < len(self.tokens):
                return self.tokens[self.pos]
            return None
        
        def consume(self):
            token = self.peek()
            self.pos += 1
            return token
        
        def expect(self, token):
            if self.peek() != token:
                raise ValueError(f"Expected {token}, got {self.peek()}")
            return self.consume()
    
    def tokenize(expr_str):
        """Tokenize an expression string."""
        tokens = []
        i = 0
        while i < len(expr_str):
            if expr_str[i].isspace():
                i += 1
            elif expr_str[i] in '()+-*/%=<>!':
                if i + 1 < len(expr_str):
                    two_char = expr_str[i:i+2]
                    if two_char in ['==', '!=', '<=', '>=']:
                        tokens.append(two_char)
                        i += 2
                        continue
                tokens.append(expr_str[i])
                i += 1
            elif expr_str[i].isdigit():
                j = i
                while j < len(expr_str) and expr_str[j].isdigit():
                    j += 1
                tokens.append(int(expr_str[i:j]))
                i = j
            elif expr_str[i].isalpha() or expr_str[i] == '_':
                j = i
                while j < len(expr_str) and (expr_str[j].isalnum() or expr_str[j] == '_'):
                    j += 1
                tokens.append(expr_str[i:j])
                i = j
            else:
                raise ValueError(f"Unknown character: {expr_str[i]}")
        return tokens
    
    def parse_expression(tokens):
        """Parse an expression with operator precedence."""
        parser = Parser(tokens)
        result = parse_comparison(parser)
        if parser.peek() is not None:
            raise ValueError(f"Unexpected token: {parser.peek()}")
        return result
    
    def parse_comparison(parser):
        """Parse comparison operators (lowest precedence)."""
        left = parse_additive(parser)
        while parser.peek() in ['==', '!=', '<', '<=', '>', '>=']:
            op = parser.consume()
            right = parse_additive(parser)
            if op == '==':
                left = 1 if left == right else 0
            elif op == '!=':
                left = 1 if left != right else 0
            elif op == '<':
                left = 1 if left < right else 0
            elif op == '<=':
                left = 1 if left <= right else 0
            elif op == '>':
                left = 1 if left > right else 0
            elif op == '>=':
                left = 1 if left >= right else 0
        return left
    
    def parse_additive(parser):
        """Parse + and - operators."""
        left = parse_multiplicative(parser)
        while parser.peek() in ['+', '-']:
            op = parser.consume()
            right = parse_multiplicative(parser)
            if op == '+':
                left = left + right
            else:
                left = left - right
        return left
    
    def parse_multiplicative(parser):
        """Parse *, /, % operators."""
        left = parse_primary(parser)
        while parser.peek() in ['*', '/', '%']:
            op = parser.consume()
            right = parse_primary(parser)
            if op == '*':
                left = left * right
            elif op == '/':
                if right == 0:
                    raise ValueError("Division by zero")
                left = left // right
            elif op == '%':
                if right == 0:
                    raise ValueError("Modulo by zero")
                left = left % right
        return left
    
    def parse_primary(parser):
        """Parse primary expressions: numbers, variables, parentheses."""
        token = parser.peek()
        
        if token is None:
            raise ValueError("Unexpected end of expression")
        
        if isinstance(token, int):
            parser.consume()
            return token
        
        if isinstance(token, str):
            if token == '(':
                parser.consume()
                result = parse_comparison(parser)
                if parser.peek() != ')':
                    raise ValueError("Unbalanced parentheses")
                parser.consume()
                return result
            elif token.isalpha() or token == '_':
                parser.consume()
                if token not in variables:
                    raise ValueError(f"Undefined variable: {token}")
                return variables[token]
            else:
                raise ValueError(f"Unexpected token: {token}")
        
        raise ValueError(f"Unexpected token: {token}")
    
    def evaluate_expression(expr_str):
        """Evaluate an expression string."""
        tokens = tokenize(expr_str)
        if not tokens:
            raise ValueError("Empty expression")
        return parse_expression(tokens)
    
    def execute_block(line_idx, end_idx):
        """Execute a block of statements from line_idx to end_idx."""
        while line_idx < end_idx:
            line = lines[line_idx]
            line_idx += 1
            
            # Skip empty lines
            if not line:
                continue
            
            # Handle if statement
            if line.startswith('if '):
                cond_str = line[3:]
                if cond_str.endswith('{'):
                    cond_str = cond_str[:-1].strip()
                else:
                    raise ValueError("Expected '{' after if condition")
                
                cond_value = evaluate_expression(cond_str)
                
                # Find matching closing brace
                block_start = line_idx
                brace_count = 1
                block_end = block_start
                while block_end < len(lines) and brace_count > 0:
                    if lines[block_end] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    elif lines[block_end].endswith('{'):
                        brace_count += 1
                    block_end += 1
                
                if brace_count != 0:
                    raise ValueError("Unbalanced braces")
                
                # Check for else
                else_start = block_end + 1
                has_else = False
                else_block_end = else_start
                
                if else_start < len(lines):
                    next_line = lines[else_start]
                    if next_line == 'else {' or (block_end < len(lines) - 1 and lines[block_end] == '}' and else_start < len(lines) and lines[else_start] == 'else {'):
                        has_else = True
                        # Find matching closing brace for else
                        brace_count = 1
                        else_block_end = else_start + 1
                        while else_block_end < len(lines) and brace_count > 0:
                            if lines[else_block_end] == '}':
                                brace_count -= 1
                            elif lines[else_block_end].endswith('{'):
                                brace_count += 1
                            else_block_end += 1
                
                # Execute if or else block
                if cond_value != 0:
                    execute_block(block_start, block_end)
                elif has_else:
                    execute_block(else_start + 1, else_block_end - 1)
                
                # Skip to after the if/else block
                if has_else:
                    line_idx = else_block_end
                else:
                    line_idx = block_end + 1
                continue
            
            # Handle while statement
            if line.startswith('while '):
                cond_str = line[6:]
                if cond_str.endswith('{'):
                    cond_str = cond_str[:-1].strip()
                else:
                    raise ValueError("Expected '{' after while condition")
                
                # Find matching closing brace
                block_start = line_idx
                brace_count = 1
                block_end = block_start
                while block_end < len(lines) and brace_count > 0:
                    if lines[block_end] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    elif lines[block_end].endswith('{'):
                        brace_count += 1
                    block_end += 1
                
                if brace_count != 0:
                    raise ValueError("Unbalanced braces")
                
                # Execute while loop
                while True:
                    cond_value = evaluate_expression(cond_str)
                    if cond_value == 0:
                        break
                    execute_block(block_start, block_end)
                
                line_idx = block_end + 1
                continue
            
            # Handle closing brace (should not appear here)
            if line == '}':
                raise ValueError("Stray closing brace")
            
            # Handle print statement
            if line.startswith('print('):
                if not line.endswith(')'):
                    raise ValueError("Unbalanced parentheses")
                expr_str = line[6:-1]
                value = evaluate_expression(expr_str)
                output.append(str(value) + '\n')
                continue
            
            # Handle assignment
            if '=' in line:
                parts = line.split('=', 1)
                if len(parts) != 2:
                    raise ValueError("Invalid assignment")
                
                var_name = parts[0].strip()
                rhs = parts[1].strip()
                
                if not var_name or not var_name.replace('_', '').isalnum():
                    raise ValueError("Invalid variable name")
                
                # Check if it's input()
                if rhs == 'input()':
                    if input_index[0] >= len(inputs):
                        raise ValueError("No more inputs")
                    variables[var_name] = inputs[input_index[0]]
                    input_index[0] += 1
                else:
                    value = evaluate_expression(rhs)
                    variables[var_name] = value
                continue
            
            raise ValueError(f"Unknown statement: {line}")
        
        return line_idx
    
    try:
        execute_block(0, len(lines))
    except ValueError:
        raise
    
    return ''.join(output)
