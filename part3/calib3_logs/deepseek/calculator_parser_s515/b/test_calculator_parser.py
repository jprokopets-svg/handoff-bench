from calculator_parser import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert evaluate('2 + 3 * 4') == 14.0

assert evaluate('(2 + 3) * 4') == 20.0

assert evaluate('2 ** 3 ** 2') == 512.0

assert evaluate('-2 ** 2') == -4.0

assert evaluate('2 ** -1') == 0.5

assert evaluate('10 % 3') == 1.0

assert evaluate('-7 % 3') == 2.0

assert evaluate('3.5 * 2') == 7.0

assert evaluate('7 / 2') == 3.5

assert evaluate('  - 5 + 2 ') == -3.0

assert evaluate('2 * -3') == -6.0

assert evaluate('(1 + 2) ** (3 - 1)') == 9.0

assert evaluate('+3') == 3.0

assert _raises(lambda: evaluate('1 / 0'))

assert _raises(lambda: evaluate('1 % 0'))

assert _raises(lambda: evaluate('((1+2)'))

assert _raises(lambda: evaluate(''))

assert _raises(lambda: evaluate('1 2'))

assert _raises(lambda: evaluate('1+'))

assert _raises(lambda: evaluate('2**'))

assert _raises(lambda: evaluate('a'))