class TCPStateMachine:
    def __init__(self):
        self.state = 'CLOSED'
        self.transitions = {
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

    def handle(self, event):
        if (self.state, event) in self.transitions:
            self.state = self.transitions[(self.state, event)]
            return self.state
        else:
            raise ValueError("Invalid transition")
