class TCPStateMachine:
    def __init__(self):
        self._state = 'CLOSED'
        
    @property
    def state(self):
        return self._state
    
    def handle(self, event):
        # Define all valid transitions
        transitions = {
            ('CLOSED', 'OPEN'): 'LISTEN',
            ('CLOSED', 'SYN'): 'SYN_SENT',
            ('LISTEN', 'SYN'): 'SYN_RCVD',
            ('LISTEN', 'RESET'): 'LISTEN',
            ('SYN_SENT', 'SYN_ACK'): 'ESTABLISHED',
            ('SYN_SENT', 'SYN'): 'SYN_RCVD',
            ('SYN_SENT', 'RESET'): 'CLOSED',
            ('SYN_RCVD', 'ACK'): 'ESTABLISHED',
            ('SYN_RCVD', 'CLOSE'): 'FIN_WAIT_1',
            ('ESTABLISHED', 'FIN'): 'CLOSE_WAIT',
            ('ESTABLISHED', 'CLOSE'): 'FIN_WAIT_1',
            ('ESTABLISHED', 'RESET'): 'CLOSED',
            ('FIN_WAIT_1', 'ACK'): 'FIN_WAIT_2',
            ('FIN_WAIT_1', 'FIN'): 'CLOSING',
            ('FIN_WAIT_1', 'FIN_ACK'): 'TIME_WAIT',
            ('FIN_WAIT_2', 'FIN'): 'TIME_WAIT',
            ('CLOSING', 'ACK'): 'TIME_WAIT',
            ('CLOSE_WAIT', 'CLOSE'): 'LAST_ACK',
            ('LAST_ACK', 'ACK'): 'CLOSED',
            ('TIME_WAIT', 'TIMEOUT'): 'CLOSED',
            ('TIME_WAIT', 'RESET'): 'CLOSED',
        }
        
        key = (self._state, event)
        if key in transitions:
            self._state = transitions[key]
            return self._state
        else:
            raise ValueError