import threading


class Bank:
    def __init__(self):
        """Initialize the bank with an empty accounts dictionary and a lock for thread safety."""
        self._accounts = {}
        self._lock = threading.Lock()

    def create_account(self, acc_id: str) -> None:
        """
        Create a new account with the given account ID.
        
        Args:
            acc_id: The account identifier (string)
            
        Raises:
            ValueError: If the account already exists
        """
        with self._lock:
            if acc_id in self._accounts:
                raise ValueError(f"Account '{acc_id}' already exists")
            self._accounts[acc_id] = 0.0

    def deposit(self, acc_id: str, amount: float) -> None:
        """
        Deposit money into an account.
        
        Args:
            acc_id: The account identifier
            amount: The amount to deposit (must be positive)
            
        Raises:
            ValueError: If amount <= 0, account doesn't exist
        """
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}")
        
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account '{acc_id}' does not exist")
            self._accounts[acc_id] += amount

    def withdraw(self, acc_id: str, amount: float) -> None:
        """
        Withdraw money from an account.
        
        Args:
            acc_id: The account identifier
            amount: The amount to withdraw (must be positive)
            
        Raises:
            ValueError: If amount <= 0, account doesn't exist, or insufficient funds
        """
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive, got {amount}")
        
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account '{acc_id}' does not exist")
            if self._accounts[acc_id] < amount:
                raise ValueError(f"Insufficient funds in account '{acc_id}'")
            self._accounts[acc_id] -= amount

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        """
        Atomically transfer money from one account to another.
        
        Args:
            from_id: Source account identifier
            to_id: Destination account identifier
            amount: The amount to transfer (must be positive)
            
        Raises:
            ValueError: If amount <= 0, either account doesn't exist, or insufficient funds
                       (in which case NOTHING changes)
        """
        if amount <= 0:
            raise ValueError(f"Transfer amount must be positive, got {amount}")
        
        with self._lock:
            # Check both accounts exist before any state change
            if from_id not in self._accounts:
                raise ValueError(f"Account '{from_id}' does not exist")
            if to_id not in self._accounts:
                raise ValueError(f"Account '{to_id}' does not exist")
            
            # Check sufficient funds before any state change
            if self._accounts[from_id] < amount:
                raise ValueError(f"Insufficient funds in account '{from_id}'")
            
            # Perform atomic transfer
            self._accounts[from_id] -= amount
            self._accounts[to_id] += amount

    def balance(self, acc_id: str) -> float:
        """
        Get the balance of an account.
        
        Args:
            acc_id: The account identifier
            
        Returns:
            The account balance
            
        Raises:
            ValueError: If account doesn't exist
        """
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account '{acc_id}' does not exist")
            return self._accounts[acc_id]
