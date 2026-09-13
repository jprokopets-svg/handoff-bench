from mini_interpreter import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert run_program('x = 5\nprint(x)') == '5\n'

assert run_program('print(2 + 3 * 4)') == '14\n'

assert run_program('print((2 + 3) * 4)') == '20\n'

assert run_program('print(10 % 3)') == '1\n'

assert run_program('print(20 / 4)') == '5\n'

assert run_program('x = 10\ny = x - 3\nprint(y)') == '7\n'

assert run_program('print(2 * 3 == 6)') == '1\n'

assert run_program('print(2 * 3 == 7)') == '0\n'

assert run_program('if 3 > 2 {\nprint(1)\n}') == '1\n'

assert run_program('if 0 {\nprint(1)\n} else {\nprint(2)\n}') == '2\n'

assert run_program('x = 0\nwhile x < 3 {\nx = x + 1\nprint(x)\n}') == '1\n2\n3\n'

assert run_program('x = 1\nwhile x <= 10 {\nprint(x)\nx = x * 2\n}') == '1\n2\n4\n8\n'

assert run_program('x = input()\nprint(x + 1)', [41]) == '42\n'

assert run_program('a = 1\nb = 2\nif a < b {\nprint(a + b)\n} else {\nprint(0)\n}') == '3\n'

assert run_program('x = 5\nx = x * 2\nprint(x)') == '10\n'

assert run_program('i = 0\ns = 0\nwhile i < 5 {\ns = s + i\ni = i + 1\n}\nprint(s)') == '10\n'

assert _raises(lambda: run_program('print(x)'))

assert _raises(lambda: run_program('print(1 / 0)'))

assert _raises(lambda: run_program('print(1 % 0)'))

assert _raises(lambda: run_program('x = 1\nif x {'))

assert _raises(lambda: run_program('}'))

assert _raises(lambda: run_program('print(1 2)'))

assert _raises(lambda: run_program('print(1 +)'))

assert _raises(lambda: run_program('print(x)', [1]))

assert _raises(lambda: run_program('print((1)'))

assert _raises(lambda: run_program('x = = 1'))