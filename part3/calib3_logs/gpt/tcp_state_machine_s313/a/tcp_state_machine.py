class TCPStateMachine:
    def __init__(self):
        self.state = 'CLOSED'

        # Define valid transitions as mapping (state, event) -> new_state
        self._transitions = {
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
        key = (self.state, event)
        if key not in self._transitions:
            raise ValueError(f"Invalid transition: ({self.state}, {event})")
        new_state = self._transitions[key]
        self.state = new_state
        return self.state
