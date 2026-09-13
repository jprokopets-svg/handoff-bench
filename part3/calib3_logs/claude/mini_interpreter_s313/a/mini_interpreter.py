def run_program(src: str, inputs: list | None = None) -> str:
    """
    Execute a tiny imperative programming language.
    Returns concatenated output of all print statements.
    """
    if inputs is None:
        inputs = []
    
    lines = src.split('\n')
    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    
    output = []
    variables = {}
    input_index = [0]  # Use list to allow modification in nested functions
    
    def get_input():
        if input_index[0] >= len(inputs):
            raise ValueError("input() called with no inputs left")
        val = inputs[input_index[0]]
        input_index[0] += 1
        return val
    
    def tokenize(expr: str):
        """Tokenize an expression string."""
        tokens = []
        i = 0
        while i < len(expr):
            if expr[i].isspace():
                i += 1
            elif expr[i] in '()+-*/%':
                tokens.append(expr[i])
                i += 1
            elif expr[i:i+2] == '==':
                tokens.append('==')
                i += 2
            elif expr[i:i+2] == '!=':
                tokens.append('!=')
                i += 2
            elif expr[i:i+2] == '<=':
                tokens.append('<=')
                i += 2
            elif expr[i:i+2] == '>=':
                tokens.append('>=')
                i += 2
            elif expr[i] in '<>':
                tokens.append(expr[i])
                i += 1
            elif expr[i].isdigit():
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append(int(expr[i:j]))
                i = j
            elif expr[i].isalpha() or expr[i] == '_':
                j = i
                while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
            else:
                raise ValueError(f"Unexpected character: {expr[i]}")
        return tokens
    
    def parse_expr(tokens):
        """Parse and evaluate an expression. Returns (value, remaining_tokens)."""
        value, tokens = parse_comparison(tokens)
        return value, tokens
    
    def parse_comparison(tokens):
        """Parse comparison operators (lowest precedence among binary ops)."""
        left, tokens = parse_additive(tokens)
        
        while tokens and tokens[0] in ['==', '!=', '<', '<=', '>', '>=']:
            op = tokens[0]
            tokens = tokens[1:]
            right, tokens = parse_additive(tokens)
            
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
        
        return left, tokens
    
    def parse_additive(tokens):
        """Parse + and - operators."""
        left, tokens = parse_multiplicative(tokens)
        
        while tokens and tokens[0] in ['+', '-']:
            op = tokens[0]
            tokens = tokens[1:]
            right, tokens = parse_multiplicative(tokens)
            
            if op == '+':
                left = left + right
            else:
                left = left - right
        
        return left, tokens
    
    def parse_multiplicative(tokens):
        """Parse *, /, % operators."""
        left, tokens = parse_primary(tokens)
        
        while tokens and tokens[0] in ['*', '/', '%']:
            op = tokens[0]
            tokens = tokens[1:]
            right, tokens = parse_primary(tokens)
            
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
        
        return left, tokens
    
    def parse_primary(tokens):
        """Parse primary expressions (numbers, variables, parentheses)."""
        if not tokens:
            raise ValueError("Unexpected end of expression")
        
        token = tokens[0]
        
        if isinstance(token, int):
            return token, tokens[1:]
        elif isinstance(token, str) and token.isalpha():
            # Variable
            if token not in variables:
                raise ValueError(f"Undefined variable: {token}")
            return variables[token], tokens[1:]
        elif token == '(':
            tokens = tokens[1:]
            value, tokens = parse_expr(tokens)
            if not tokens or tokens[0] != ')':
                raise ValueError("Unbalanced parentheses")
            return value, tokens[1:]
        else:
            raise ValueError(f"Unexpected token: {token}")
    
    def evaluate_expr(expr_str: str):
        """Evaluate an expression string."""
        tokens = tokenize(expr_str)
        if not tokens:
            raise ValueError("Empty expression")
        value, remaining = parse_expr(tokens)
        if remaining:
            raise ValueError(f"Unexpected tokens after expression: {remaining}")
        return value
    
    def execute_block(line_idx):
        """Execute a block of statements. Returns the index after the closing brace."""
        while line_idx < len(lines):
            line = lines[line_idx]
            
            if line == '}':
                return line_idx + 1
            
            if line.startswith('if '):
                line_idx = execute_if(line_idx)
            elif line.startswith('while '):
                line_idx = execute_while(line_idx)
            elif line.startswith('print('):
                execute_print(line)
                line_idx += 1
            elif '=' in line:
                execute_assignment(line)
                line_idx += 1
            else:
                raise ValueError(f"Unknown statement: {line}")
        
        return line_idx
    
    def execute_if(line_idx):
        """Execute an if statement. Returns the index after the if/else block."""
        line = lines[line_idx]
        
        # Parse: if COND {
        if not line.startswith('if '):
            raise ValueError("Expected 'if'")
        
        rest = line[3:].strip()
        if not rest.endswith('{'):
            raise ValueError("Expected '{' after if condition")
        
        cond_str = rest[:-1].strip()
        cond_value = evaluate_expr(cond_str)
        
        line_idx += 1
        
        # Execute if block
        if_block_start = line_idx
        if_block_end = find_block_end(line_idx)
        
        if cond_value != 0:
            # Execute if block
            execute_block_range(if_block_start, if_block_end)
        
        line_idx = if_block_end + 1  # Move past '}'
        
        # Check for else
        if line_idx < len(lines):
            next_line = lines[line_idx]
            if next_line == 'else {':
                line_idx += 1
                else_block_start = line_idx
                else_block_end = find_block_end(line_idx)
                
                if cond_value == 0:
                    # Execute else block
                    execute_block_range(else_block_start, else_block_end)
                
                line_idx = else_block_end + 1
            elif next_line.startswith('} else {'):
                # This shouldn't happen if we're parsing correctly
                pass
        
        return line_idx
    
    def execute_while(line_idx):
        """Execute a while loop. Returns the index after the loop."""
        line = lines[line_idx]
        
        # Parse: while COND {
        if not line.startswith('while '):
            raise ValueError("Expected 'while'")
        
        rest = line[6:].strip()
        if not rest.endswith('{'):
            raise ValueError("Expected '{' after while condition")
        
        cond_str = rest[:-1].strip()
        
        loop_body_start = line_idx + 1
        loop_body_end = find_block_end(loop_body_start)
        
        # Execute while loop
        while True:
            cond_value = evaluate_expr(cond_str)
            if cond_value == 0:
                break
            execute_block_range(loop_body_start, loop_body_end)
        
        return loop_body_end + 1
    
    def find_block_end(start_idx):
        """Find the index of the closing '}' for a block starting at start_idx."""
        depth = 1
        idx = start_idx
        while idx < len(lines):
            line = lines[idx]
            if line == '{':
                depth += 1
            elif line == '}':
                depth -= 1
                if depth == 0:
                    return idx
            elif line.endswith('{'):
                depth += 1
            elif line.startswith('}'):
                depth -= 1
                if depth == 0:
                    return idx
            idx += 1
        raise ValueError("Unbalanced braces")
    
    def execute_block_range(start_idx, end_idx):
        """Execute statements from start_idx to end_idx (exclusive)."""
        idx = start_idx
        while idx < end_idx:
            line = lines[idx]
            
            if line == '}':
                raise ValueError("Unexpected '}'")
            
            if line.startswith('if '):
                idx = execute_if(idx)
            elif line.startswith('while '):
                idx = execute_while(idx)
            elif line.startswith('print('):
                execute_print(line)
                idx += 1
            elif '=' in line:
                execute_assignment(line)
                idx += 1
            else:
                raise ValueError(f"Unknown statement: {line}")
    
    def execute_print(line):
        """Execute a print statement."""
        if not line.startswith('print(') or not line.endswith(')'):
            raise ValueError("Invalid print statement")
        
        expr_str = line[6:-1]
        value = evaluate_expr(expr_str)
        output.append(str(value) + '\n')
    
    def execute_assignment(line):
        """Execute an assignment statement."""
        if '=' not in line:
            raise ValueError("Expected '=' in assignment")
        
        parts = line.split('=', 1)
        if len(parts) != 2:
            raise ValueError("Invalid assignment")
        
        var_name = parts[0].strip()
        expr_str = parts[1].strip()
        
        if not var_name or not var_name.isalpha():
            raise ValueError(f"Invalid variable name: {var_name}")
        
        # Check for input()
        if expr_str == 'input()':
            variables[var_name] = get_input()
        else:
            value = evaluate_expr(expr_str)
            variables[var_name] = value
    
    # Main execution
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        
        if line == '}':
            raise ValueError("Unexpected '}'")
        
        if line.startswith('if '):
            idx = execute_if(idx)
        elif line.startswith('while '):
            idx = execute_while(idx)
        elif line.startswith('print('):
            execute_print(line)
            idx += 1
        elif '=' in line:
            execute_assignment(line)
            idx += 1
        else:
            raise ValueError(f"Unknown statement: {line}")
    
    return ''.join(output)
