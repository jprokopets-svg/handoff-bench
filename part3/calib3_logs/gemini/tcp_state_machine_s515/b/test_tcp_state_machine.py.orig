from tcp_state_machine import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

m = TCPStateMachine(); assert m.state == 'CLOSED'

m = TCPStateMachine(); assert m.handle('SYN') == 'SYN_SENT'

m = TCPStateMachine(); assert m.handle('OPEN') == 'LISTEN'

m = TCPStateMachine(); m.handle('OPEN'); assert m.handle('SYN') == 'SYN_RCVD'

m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); assert m.handle('ACK') == 'ESTABLISHED'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); assert m.state == 'ESTABLISHED'

m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); assert m.handle('FIN') == 'CLOSE_WAIT'

m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); m.handle('FIN'); assert m.handle('CLOSE') == 'LAST_ACK'

m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); m.handle('FIN'); m.handle('CLOSE'); assert m.handle('ACK') == 'CLOSED'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); assert m.state == 'FIN_WAIT_1'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('ACK'); assert m.handle('FIN') == 'TIME_WAIT'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('ACK'); m.handle('FIN'); assert m.handle('TIMEOUT') == 'CLOSED'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); assert m.handle('FIN') == 'CLOSING'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('FIN'); assert m.handle('ACK') == 'TIME_WAIT'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('FIN_ACK'); assert m.state == 'TIME_WAIT'

m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('FIN'); m.handle('ACK'); m.handle('TIMEOUT'); assert m.state == 'CLOSED'

m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); assert _raises(lambda: m.handle('SYN'))

m = TCPStateMachine(); m.handle('SYN'); assert _raises(lambda: m.handle('ACK'))

m = TCPStateMachine(); assert _raises(lambda: m.handle('FIN'))

m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); m.handle('FIN'); assert _raises(lambda: m.handle('ACK'))