import threading

class Bank:
    def __init__(self):
        # single lock to make all operations atomic and thread-safe
        self._lock = threading.RLock()
        self._accounts = {}

    def create_account(self, acc_id: str) -> None:
        with self._lock:
            if acc_id in self._accounts:
                raise ValueError("account already exists")
            self._accounts[acc_id] = 0.0

    def deposit(self, acc_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError("account does not exist")
            # safe to add
            self._accounts[acc_id] += float(amount)

    def withdraw(self, acc_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError("account does not exist")
            if self._accounts[acc_id] < amount:
                raise ValueError("insufficient funds")
            self._accounts[acc_id] -= float(amount)

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            if from_id not in self._accounts or to_id not in self._accounts:
                raise ValueError("account does not exist")
            if self._accounts[from_id] < amount:
                raise ValueError("insufficient funds")
            # perform transfer atomically
            self._accounts[from_id] -= float(amount)
            self._accounts[to_id] += float(amount)

    def balance(self, acc_id: str) -> float:
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError("account does not exist")
            return float(self._accounts[acc_id])
