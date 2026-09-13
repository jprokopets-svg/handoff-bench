class TCPStateMachine:
    def __init__(self):
        self.state = 'CLOSED'
        # Define the state transition table
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
    
    def handle(self, event: str) -> str:
        """
        Handle an event and transition to a new state.
        
        Args:
            event: The event to handle
            
        Returns:
            The new state after the transition
            
        Raises:
            ValueError: If the (current state, event) pair is not in the transition table
        """
        key = (self.state, event)
        if key not in self.transitions:
            raise ValueError(f"Invalid transition from {self.state} with event {event}")
        
        self.state = self.transitions[key]
        return self.state
