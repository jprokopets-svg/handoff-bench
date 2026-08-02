from mini_brainfuck import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert brainfuck('') == ''

assert brainfuck('+++.') == chr(3)

assert brainfuck('++[>+<-]>.') == chr(2)

assert brainfuck('+++[>+.<-]') == chr(1) + chr(2) + chr(3)

assert brainfuck('+++[->++<]>.' ) == chr(6)

assert brainfuck('++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.') == 'Hello World!\n'

assert brainfuck(',.', 'Z') == 'Z'

assert brainfuck(',+++.', 'B') == 'E'

assert brainfuck('+++.junk-+-', '') == chr(3)

assert _raises(lambda: brainfuck('['))

assert _raises(lambda: brainfuck(']'))

assert _raises(lambda: brainfuck('++[>++'))