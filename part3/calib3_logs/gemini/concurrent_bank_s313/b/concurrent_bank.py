
import threading

class Bank:
    def __init__(self):
        self._balances = {}
        self._locks = {}
        self._lock = threading.Lock()  # For creating accounts

    def create_account(self, acc_id: str) -> None:
        with self._lock:
            if acc_id in self._balances:
                raise ValueError(f"Account {acc_id} already exists")
            self._balances[acc_id] = 0.0
            self._locks[acc_id] = threading.Lock()

    def deposit(self, acc_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        with self._lock:
            if acc_id not in self._balances:
                raise ValueError(f"Account {acc_id} does not exist")
            account_lock = self._locks[acc_id]

        with account_lock:
            self._balances[acc_id] += amount

    def withdraw(self, acc_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        with self._lock:
            if acc_id not in self._balances:
                raise ValueError(f"Account {acc_id} does not exist")
            account_lock = self._locks[acc_id]

        with account_lock:
            if self._balances[acc_id] < amount:
                raise ValueError("Insufficient funds")
            self._balances[acc_id] -= amount

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if from_id == to_id:
            return

        with self._lock:
            if from_id not in self._balances:
                raise ValueError(f"Account {from_id} does not exist")
            if to_id not in self._balances:
                raise ValueError(f"Account {to_id} does not exist")

            from_lock = self._locks[from_id]
            to_lock = self._locks[to_id]

        # Deadlock avoidance
        lock_first, lock_second = (from_lock, to_lock) if from_id < to_id else (to_lock, from_lock)

        with lock_first:
            with lock_second:
                if self._balances[from_id] < amount:
                    raise ValueError("Insufficient funds for transfer")
                self._balances[from_id] -= amount
                self._balances[to_id] += amount

    def balance(self, acc_id: str) -> float:
        with self._lock:
            if acc_id not in self._balances:
                raise ValueError(f"Account {acc_id} does not exist")
            account_lock = self._locks[acc_id]
        
        with account_lock:
            return self._balances[acc_id]
