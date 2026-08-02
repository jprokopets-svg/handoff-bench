import re
from typing import List, Tuple, Any

TOKEN_REGEX = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|(\*\*)|(\+)|(-)|(\*)|(/)|(%)|(\()|(\)))")


def evaluate(expr: str) -> float:
    """Evaluate an infix arithmetic expression and return the numeric result as a float.

    Raises ValueError on invalid input or invalid operations (division/modulo by zero,
    unbalanced parentheses, invalid tokens, etc.).
    """
    try:
        if expr is None:
            raise ValueError("Empty expression")
        s = expr
        tokens: List[Tuple[str, Any]] = []
        i = 0
        length = len(s)
        # Tokenize by scanning to ensure invalid tokens are detected
        while i < length:
            m = TOKEN_REGEX.match(s, i)
            if not m:
                # If current char is whitespace, skip it, else invalid
                if s[i].isspace():
                    i += 1
                    continue
                raise ValueError("Invalid token")
            # matched groups: 1:number,2:**,3:+,4:-,5:*,6:/,7:%,8:(,9:)
            num, powop, plus, minus, mul, div, mod, lpar, rpar = m.groups()
            if num is not None:
                tokens.append(("NUMBER", float(num)))
            elif powop is not None:
                tokens.append(("POW", None))
            elif plus is not None:
                tokens.append(("PLUS", None))
            elif minus is not None:
                tokens.append(("MINUS", None))
            elif mul is not None:
                tokens.append(("MUL", None))
            elif div is not None:
                tokens.append(("DIV", None))
            elif mod is not None:
                tokens.append(("MOD", None))
            elif lpar is not None:
                tokens.append(("LPAREN", None))
            elif rpar is not None:
                tokens.append(("RPAREN", None))
            i = m.end()
        if not tokens:
            raise ValueError("Empty expression")

        pos = 0

        def peek():
            return tokens[pos] if pos < len(tokens) else ("EOF", None)

        def advance():
            nonlocal pos
            tok = peek()
            pos += 1
            return tok

        def expect(kind: str):
            tok = peek()
            if tok[0] != kind:
                raise ValueError(f"Expected {kind}")
            advance()

        # Grammar:
        # expr -> add_sub
        # add_sub -> mul_div ( (PLUS|MINUS) mul_div )*
        # mul_div -> unary ( (MUL|DIV|MOD) unary )*
        # unary -> PLUS unary | MINUS unary | power
        # power -> primary ( POW unary )?
        # primary -> NUMBER | LPAREN expr RPAREN

        def parse_primary() -> float:
            tok = peek()
            if tok[0] == "NUMBER":
                advance()
                return tok[1]
            if tok[0] == "LPAREN":
                advance()
                val = parse_expr()
                if peek()[0] != "RPAREN":
                    raise ValueError("Mismatched parenthesis")
                advance()
                return val
            raise ValueError("Expected number or '('")

        def parse_power() -> float:
            # primary (** unary)? with right-associativity
            base = parse_primary()
            if peek()[0] == "POW":
                advance()
                exponent = parse_unary()
                try:
                    return base ** exponent
                except Exception as e:
                    # re-raise as ValueError
                    raise ValueError("Invalid power operation")
            return base

        def parse_unary() -> float:
            tok = peek()
            if tok[0] == "PLUS":
                advance()
                return parse_unary()
            if tok[0] == "MINUS":
                advance()
                return -parse_unary()
            return parse_power()

        def parse_mul_div() -> float:
            val = parse_unary()
            while True:
                tok = peek()
                if tok[0] == "MUL":
                    advance()
                    rhs = parse_unary()
                    val = val * rhs
                elif tok[0] == "DIV":
                    advance()
                    rhs = parse_unary()
                    if rhs == 0:
                        raise ValueError("Division by zero")
                    val = val / rhs
                elif tok[0] == "MOD":
                    advance()
                    rhs = parse_unary()
                    if rhs == 0:
                        raise ValueError("Modulo by zero")
                    val = val % rhs
                else:
                    break
            return val

        def parse_add_sub() -> float:
            val = parse_mul_div()
            while True:
                tok = peek()
                if tok[0] == "PLUS":
                    advance()
                    val = val + parse_mul_div()
                elif tok[0] == "MINUS":
                    advance()
                    val = val - parse_mul_div()
                else:
                    break
            return val

        def parse_expr() -> float:
            return parse_add_sub()

        result = parse_expr()
        if peek()[0] != "EOF":
            # Extra tokens left like two numbers in a row or trailing operator
            raise ValueError("Unexpected token at end")
        return float(result)
    except ValueError:
        # Pass through intended ValueErrors
        raise
    except Exception as e:
        # Map other errors to ValueError
        raise ValueError(str(e))
