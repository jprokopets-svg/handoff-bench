
import threading

class Bank:
    def __init__(self):
        self.balances = {}
        self.lock = threading.Lock()

    def create_account(self, acc_id):
        with self.lock:
            if acc_id in self.balances:
                raise ValueError("Account already exists")
            self.balances[acc_id] = 0.0

    def deposit(self, acc_id, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        with self.lock:
            if acc_id not in self.balances:
                raise ValueError("Account does not exist")
            self.balances[acc_id] += amount

    def withdraw(self, acc_id, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        with self.lock:
            if acc_id not in self.balances:
                raise ValueError("Account does not exist")
            if self.balances[acc_id] < amount:
                raise ValueError("Insufficient funds")
            self.balances[acc_id] -= amount

    def transfer(self, from_id, to_id, amount):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        with self.lock:
            if from_id not in self.balances or to_id not in self.balances:
                raise ValueError("One or both accounts do not exist")
            if self.balances[from_id] < amount:
                raise ValueError("Insufficient funds")
            self.balances[from_id] -= amount
            self.balances[to_id] += amount

    def balance(self, acc_id):
        with self.lock:
            if acc_id not in self.balances:
                raise ValueError("Account does not exist")
            return self.balances[acc_id]

