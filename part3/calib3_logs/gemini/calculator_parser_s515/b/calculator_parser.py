
import ast
import operator as op

# Mapping of ast nodes to operator functions
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod
}

UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg
}

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    elif isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Invalid token in expression")
        return node.value
    elif isinstance(node, ast.Num):  # Compatibility for older Python
        return node.n
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        try:
            return OPERATORS[type(node.op)](left, right)
        except ZeroDivisionError:
            raise ValueError("Division or modulo by zero")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        return UNARY_OPERATORS[type(node.op)](operand)
    else:
        # This will catch things like function calls, variable names, etc.
        raise ValueError("Unsupported element in expression")


def evaluate(expr: str) -> float:
    """
    Evaluates an infix arithmetic expression and returns the numeric result as a float.
    """
    if not expr.strip():
        raise ValueError("Empty expression")

    try:
        # ast.parse can throw SyntaxError for a variety of malformed expressions
        tree = ast.parse(expr, mode='eval')
        result = _eval_node(tree)
        return float(result)
    except (SyntaxError, TypeError, KeyError, NameError, RecursionError, ValueError) as e:
        # Catching a broad range of errors from ast.parse and _eval_node
        # and mapping them to ValueError as per the requirements.
        if "Division or modulo by zero" in str(e):
            raise ValueError("Division or modulo by zero") from e
        raise ValueError("Invalid expression") from e

