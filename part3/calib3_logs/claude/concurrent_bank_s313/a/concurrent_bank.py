import threading


class Bank:
    def __init__(self):
        self._lock = threading.Lock()
        self._accounts = {}  # acc_id -> balance
    
    def create_account(self, acc_id: str) -> None:
        """Create a new account. Raises ValueError if account already exists."""
        with self._lock:
            if acc_id in self._accounts:
                raise ValueError(f"Account {acc_id} already exists")
            self._accounts[acc_id] = 0.0
    
    def deposit(self, acc_id: str, amount: float) -> None:
        """Deposit amount to account. Raises ValueError if amount <= 0 or account missing."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account {acc_id} does not exist")
            self._accounts[acc_id] += amount
    
    def withdraw(self, acc_id: str, amount: float) -> None:
        """Withdraw amount from account. Raises ValueError if amount <= 0, account missing, or insufficient funds."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account {acc_id} does not exist")
            if self._accounts[acc_id] < amount:
                raise ValueError(f"Insufficient funds in account {acc_id}")
            self._accounts[acc_id] -= amount
    
    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        """Atomically transfer amount from one account to another. 
        Raises ValueError if amount <= 0, either account missing, or insufficient funds.
        If transfer fails, nothing changes."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        with self._lock:
            # Check both accounts exist
            if from_id not in self._accounts:
                raise ValueError(f"Account {from_id} does not exist")
            if to_id not in self._accounts:
                raise ValueError(f"Account {to_id} does not exist")
            
            # Check sufficient funds
            if self._accounts[from_id] < amount:
                raise ValueError(f"Insufficient funds in account {from_id}")
            
            # Perform atomic transfer
            self._accounts[from_id] -= amount
            self._accounts[to_id] += amount
    
    def balance(self, acc_id: str) -> float:
        """Get the balance of an account. Raises ValueError if account missing."""
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account {acc_id} does not exist")
            return self._accounts[acc_id]
