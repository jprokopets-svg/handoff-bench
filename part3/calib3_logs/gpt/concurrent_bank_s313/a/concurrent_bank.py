import threading

class Bank:
    def __init__(self):
        # protect accounts dict and balances
        self._lock = threading.Lock()
        self._balances = {}

    def create_account(self, acc_id: str):
        with self._lock:
            if acc_id in self._balances:
                raise ValueError("account already exists")
            self._balances[acc_id] = 0.0

    def deposit(self, acc_id: str, amount: float):
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            if acc_id not in self._balances:
                raise ValueError("account does not exist")
            self._balances[acc_id] += float(amount)

    def withdraw(self, acc_id: str, amount: float):
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            if acc_id not in self._balances:
                raise ValueError("account does not exist")
            if self._balances[acc_id] < amount:
                raise ValueError("insufficient funds")
            self._balances[acc_id] -= float(amount)

    def transfer(self, from_id: str, to_id: str, amount: float):
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            if from_id not in self._balances or to_id not in self._balances:
                raise ValueError("account does not exist")
            if self._balances[from_id] < amount:
                raise ValueError("insufficient funds")
            # perform transfer
            self._balances[from_id] -= float(amount)
            self._balances[to_id] += float(amount)

    def balance(self, acc_id: str) -> float:
        with self._lock:
            if acc_id not in self._balances:
                raise ValueError("account does not exist")
            return float(self._balances[acc_id])
