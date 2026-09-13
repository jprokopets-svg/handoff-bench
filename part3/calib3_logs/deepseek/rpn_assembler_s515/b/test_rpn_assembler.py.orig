from rpn_assembler import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert run_asm('PUSH 5\nPRINT') == '5\n'

assert run_asm('PUSH 3\nPUSH 4\nADD\nPRINT') == '7\n'

assert run_asm('PUSH 10\nPUSH 3\nSUB\nPRINT') == '7\n'

assert run_asm('PUSH 6\nPUSH 7\nMUL\nPRINT') == '42\n'

assert run_asm('PUSH 20\nPUSH 4\nDIV\nPRINT') == '5\n'

assert run_asm('PUSH 2\nNEG\nPRINT') == '-2\n'

assert run_asm('PUSH 1\nPUSH 2\nSWAP\nPRINT\nPRINT') == '1\n2\n'

assert run_asm('PUSH 3\nloop:\nDUP\nDUP\nJZ done\nPRINT\nPUSH 1\nSUB\nJMP loop\ndone:\nPRINT\nHALT') == '3\n2\n1\n0\n'

assert run_asm('PUSH 0\nPUSH 3\nloop:\nDUP\nJZ done\nSWAP\nPUSH 1\nADD\nSWAP\nPUSH 1\nSUB\nJMP loop\ndone:\nPOP\nPRINT') == '3\n'

assert run_asm('# comment\nPUSH 9\nPRINT') == '9\n'

assert run_asm('PUSH 1\nHALT\nPUSH 2\nPRINT') == ''

assert run_asm('PUSH 2\nPUSH 3\nJMP skip\nADD\nPRINT\nskip:\nMUL\nPRINT') == '6\n'

assert _raises(lambda: run_asm('PUSH 1\nADD'))

assert _raises(lambda: run_asm('PUSH 1\nPUSH 0\nDIV'))

assert _raises(lambda: run_asm('JMP nowhere'))

assert _raises(lambda: run_asm('FOO'))

assert _raises(lambda: run_asm('loop:\nloop:'))

assert _raises(lambda: run_asm('PUSH'))

assert _raises(lambda: run_asm('PUSH x'))

assert _raises(lambda: run_asm('PUSH 1\nPOP\nPOP'))

assert _raises(lambda: run_asm('PRINT'))

assert _raises(lambda: run_asm('DUP'))