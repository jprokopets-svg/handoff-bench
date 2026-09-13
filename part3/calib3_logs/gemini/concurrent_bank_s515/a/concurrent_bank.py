
import threading

class Bank:
    def __init__(self):
        self._accounts = {}
        self._lock = threading.Lock()

    def create_account(self, acc_id):
        with self._lock:
            if acc_id in self._accounts:
                raise ValueError("Account already exists")
            self._accounts[acc_id] = 0.0

    def deposit(self, acc_id, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError("Account does not exist")
            self._accounts[acc_id] += amount

    def withdraw(self, acc_id, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError("Account does not exist")
            if self._accounts[acc_id] < amount:
                raise ValueError("Insufficient funds")
            self._accounts[acc_id] -= amount

    def transfer(self, from_id, to_id, amount):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        with self._lock:
            if from_id not in self._accounts or to_id not in self._accounts:
                raise ValueError("One or both accounts do not exist")
            if self._accounts[from_id] < amount:
                raise ValueError("Insufficient funds")
            self._accounts[from_id] -= amount
            self._accounts[to_id] += amount

    def balance(self, acc_id):
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError("Account does not exist")
            return self._accounts[acc_id]
