import threading


class Bank:
    def __init__(self):
        self._lock = threading.Lock()
        self._accounts = {}  # account_id -> balance
    
    def create_account(self, acc_id):
        """Create a new account with zero balance.
        
        Raises ValueError if the account already exists.
        """
        with self._lock:
            if acc_id in self._accounts:
                raise ValueError(f"Account {acc_id} already exists")
            self._accounts[acc_id] = 0.0
    
    def deposit(self, acc_id, amount):
        """Deposit amount into the account.
        
        Raises ValueError if:
        - amount <= 0
        - account does not exist
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account {acc_id} does not exist")
            self._accounts[acc_id] += amount
    
    def withdraw(self, acc_id, amount):
        """Withdraw amount from the account.
        
        Raises ValueError if:
        - amount <= 0
        - account does not exist
        - insufficient balance (no negative balances allowed)
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account {acc_id} does not exist")
            if self._accounts[acc_id] < amount:
                raise ValueError(f"Insufficient balance in account {acc_id}")
            self._accounts[acc_id] -= amount
    
    def transfer(self, from_id, to_id, amount):
        """Atomically transfer amount from one account to another.
        
        Raises ValueError if:
        - amount <= 0
        - either account does not exist
        - insufficient balance in from_id
        
        If any condition fails, nothing changes (atomic operation).
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        with self._lock:
            # Check both accounts exist
            if from_id not in self._accounts:
                raise ValueError(f"Account {from_id} does not exist")
            if to_id not in self._accounts:
                raise ValueError(f"Account {to_id} does not exist")
            
            # Check sufficient balance
            if self._accounts[from_id] < amount:
                raise ValueError(f"Insufficient balance in account {from_id}")
            
            # Perform the transfer atomically
            self._accounts[from_id] -= amount
            self._accounts[to_id] += amount
    
    def balance(self, acc_id):
        """Get the balance of an account.
        
        Raises ValueError if account does not exist.
        """
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account {acc_id} does not exist")
            return self._accounts[acc_id]
