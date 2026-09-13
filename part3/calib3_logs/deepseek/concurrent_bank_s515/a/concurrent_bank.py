import threading
from typing import Dict


class Bank:
    def __init__(self):
        self._accounts: Dict[str, float] = {}
        self._lock = threading.Lock()

    def create_account(self, acc_id: str) -> None:
        """Create a new account with zero balance."""
        with self._lock:
            if acc_id in self._accounts:
                raise ValueError(f"Account '{acc_id}' already exists")
            self._accounts[acc_id] = 0.0

    def deposit(self, acc_id: str, amount: float) -> None:
        """Deposit amount into account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account '{acc_id}' does not exist")
            self._accounts[acc_id] += amount

    def withdraw(self, acc_id: str, amount: float) -> None:
        """Withdraw amount from account."""
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account '{acc_id}' does not exist")
            if self._accounts[acc_id] < amount:
                raise ValueError("Insufficient funds")
            self._accounts[acc_id] -= amount

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        """Transfer amount from one account to another atomically."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        with self._lock:
            if from_id not in self._accounts:
                raise ValueError(f"Account '{from_id}' does not exist")
            if to_id not in self._accounts:
                raise ValueError(f"Account '{to_id}' does not exist")
            if self._accounts[from_id] < amount:
                raise ValueError("Insufficient funds")
            self._accounts[from_id] -= amount
            self._accounts[to_id] += amount

    def balance(self, acc_id: str) -> float:
        """Return the balance of the account."""
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError(f"Account '{acc_id}' does not exist")
            return self._accounts[acc_id]