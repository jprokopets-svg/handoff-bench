import re
from typing import List, Optional, Dict, Any

def run_program(src: str, inputs: Optional[List[int]] = None) -> str:
    """Execute the program and return concatenated output of all print statements."""
    if inputs is None:
        inputs = []
    interpreter = Interpreter(src, inputs)
    interpreter.run()
    return interpreter.output

class Interpreter:
    def __init__(self, src: str, inputs: List[int]):
        self.src = src
        self.inputs = inputs
        self.input_index = 0
        self.vars: Dict[str, int] = {}
        self.output = ""
        self.lines = [line.strip() for line in src.split('\n') if line.strip() != '']
        self.line_num = 0
        self.stack: List[Dict] = []  # For tracking blocks
        
    def run(self):
        """Execute the program."""
        self.execute_block(self.lines, 0, len(self.lines))
        
    def execute_block(self, lines: List[str], start: int, end: int) -> int:
        """Execute statements from start to end-1, return next line index."""
        i = start
        while i < end:
            line = lines[i]
            i += 1
            
            # Skip empty lines
            if not line:
                continue
                
            # Check for closing brace
            if line == '}':
                # End of block
                return i
                
            # Parse statement
            i = self.execute_statement(line, lines, i, end)
            
        return i
    
    def execute_statement(self, line: str, lines: List[str], i: int, end: int) -> int:
        """Execute a single statement, return next line index."""
        # Assignment
        if '=' in line:
            # Split on first '='
            eq_pos = line.find('=')
            var_name = line[:eq_pos].strip()
            expr = line[eq_pos + 1:].strip()
            
            # Check for input()
            if expr == 'input()':
                if self.input_index >= len(self.inputs):
                    raise ValueError("No more inputs")
                value = self.inputs[self.input_index]
                self.input_index += 1
                self.vars[var_name] = value
                return i
            else:
                value = self.evaluate_expr(expr)
                self.vars[var_name] = value
                return i
                
        # Print statement
        elif line.startswith('print(') and line.endswith(')'):
            expr = line[6:-1].strip()  # Remove 'print(' and ')'
            value = self.evaluate_expr(expr)
            self.output += str(value) + '\n'
            return i
            
        # If statement
        elif line.startswith('if '):
            # Parse condition
            cond_str = line[3:].strip()
            # Remove trailing '{'
            if cond_str.endswith('{'):
                cond_str = cond_str[:-1].strip()
            else:
                # Should have '{' on same line
                raise ValueError("Missing '{' after if condition")
                
            cond_value = self.evaluate_expr(cond_str)
            
            # Execute then block
            then_end = self.find_matching_brace(lines, i-1)
            
            # Check for else
            if then_end < len(lines) and lines[then_end].strip() == '} else {':
                # Single line '} else {'
                else_start = then_end + 1
                else_end = self.find_matching_brace(lines, else_start - 1)
                if cond_value != 0:
                    # Execute then block
                    self.execute_block(lines, i, then_end)
                else:
                    # Execute else block
                    self.execute_block(lines, else_start + 1, else_end)
                return else_end + 1
            elif then_end < len(lines) and lines[then_end].strip() == '}':
                # Check if next line is 'else {'
                if then_end + 1 < len(lines) and lines[then_end + 1].strip() == 'else {':
                    else_start = then_end + 2
                    else_end = self.find_matching_brace(lines, else_start - 1)
                    if cond_value != 0:
                        self.execute_block(lines, i, then_end)
                    else:
                        self.execute_block(lines, else_start, else_end)
                    return else_end + 1
                else:
                    # No else block
                    if cond_value != 0:
                        self.execute_block(lines, i, then_end)
                    return then_end + 1
            else:
                raise ValueError("Unclosed if block")
                
        # While statement
        elif line.startswith('while '):
            # Parse condition
            cond_str = line[6:].strip()
            if cond_str.endswith('{'):
                cond_str = cond_str[:-1].strip()
            else:
                raise ValueError("Missing '{' after while condition")
                
            # Find block end
            block_start = i
            block_end = self.find_matching_brace(lines, i-1)
            
            # Execute while loop
            while True:
                cond_value = self.evaluate_expr(cond_str)
                if cond_value == 0:
                    break
                # Execute block
                # Save current position and restore after block
                saved_line_num = self.line_num
                self.execute_block(lines, block_start, block_end)
                self.line_num = saved_line_num
                
            return block_end + 1
            
        else:
            raise ValueError(f"Syntax error: {line}")
    
    def find_matching_brace(self, lines: List[str], start_idx: int) -> int:
        """Find the matching '}' for a '{' at start_idx."""
        depth = 1
        i = start_idx + 1
        while i < len(lines):
            line = lines[i].strip()
            if line == '{':
                depth += 1
            elif line == '}':
                depth -= 1
                if depth == 0:
                    return i
            elif line == '} else {':
                depth -= 1
                if depth == 0:
                    return i
            i += 1
        raise ValueError("Unmatched brace")
    
    def evaluate_expr(self, expr: str) -> int:
        """Evaluate an expression and return integer value."""
        # Remove whitespace
        expr = expr.replace(' ', '')
        
        # Handle parentheses
        return self._eval_comparison(expr)
    
    def _eval_comparison(self, expr: str) -> int:
        """Parse comparison operators (lowest precedence)."""
        # Split by comparison operators
        ops = ['==', '!=', '<=', '>=', '<', '>']
        
        for op in ops:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self._eval_add_sub(parts[0])
                    right = self._eval_add_sub(parts[1])
                    if op == '==':
                        return 1 if left == right else 0
                    elif op == '!=':
                        return 1 if left != right else 0
                    elif op == '<':
                        return 1 if left < right else 0
                    elif op == '<=':
                        return 1 if left <= right else 0
                    elif op == '>':
                        return 1 if left > right else 0
                    elif op == '>=':
                        return 1 if left >= right else 0
        
        # No comparison operator
        return self._eval_add_sub(expr)
    
    def _eval_add_sub(self, expr: str) -> int:
        """Parse + and - operators."""
        # Find the rightmost + or - that's not inside parentheses
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            c = expr[i]
            if c == ')':
                depth += 1
            elif c == '(':
                depth -= 1
            elif depth == 0 and c == '+':
                left = self._eval_add_sub(expr[:i])
                right = self._eval_mul_div_mod(expr[i+1:])
                return left + right
            elif depth == 0 and c == '-':
                left = self._eval_add_sub(expr[:i])
                right = self._eval_mul_div_mod(expr[i+1:])
                return left - right
        
        # No + or - operator
        return self._eval_mul_div_mod(expr)
    
    def _eval_mul_div_mod(self, expr: str) -> int:
        """Parse *, /, % operators."""
        # Find the rightmost *, /, % that's not inside parentheses
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            c = expr[i]
            if c == ')':
                depth += 1
            elif c == '(':
                depth -= 1
            elif depth == 0 and c == '*':
                left = self._eval_mul_div_mod(expr[:i])
                right = self._eval_factor(expr[i+1:])
                return left * right
            elif depth == 0 and c == '/':
                left = self._eval_mul_div_mod(expr[:i])
                right = self._eval_factor(expr[i+1:])
                if right == 0:
                    raise ValueError("Division by zero")
                return left // right  # Integer division
            elif depth == 0 and c == '%':
                left = self._eval_mul_div_mod(expr[:i])
                right = self._eval_factor(expr[i+1:])
                if right == 0:
                    raise ValueError("Modulo by zero")
                return left % right
        
        # No *, /, % operator
        return self._eval_factor(expr)
    
    def _eval_factor(self, expr: str) -> int:
        """Parse numbers, variables, parentheses, or input()."""
        expr = expr.strip()
        
        if not expr:
            raise ValueError("Empty expression")
        
        # Number
        if expr.isdigit():
            return int(expr)
        
        # Variable
        if expr.isidentifier():
            if expr not in self.vars:
                raise ValueError(f"Undefined variable '{expr}'")
            return self.vars[expr]
        
        # Parentheses
        if expr[0] == '(' and expr[-1] == ')':
            return self._eval_comparison(expr[1:-1])
        
        # input()
        if expr == 'input()':
            if self.input_index >= len(self.inputs):
                raise ValueError("No more inputs")
            value = self.inputs[self.input_index]
            self.input_index += 1
            return value
        
        raise ValueError(f"Invalid expression: {expr}")