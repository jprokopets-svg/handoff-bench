
import threading

class Bank:
    def __init__(self):
        self._accounts = {}
        self._lock = threading.Lock()

    def create_account(self, acc_id: str) -> None:
        with self._lock:
            if acc_id in self._accounts:
                raise ValueError("Account already exists")
            self._accounts[acc_id] = {'balance': 0.0, 'lock': threading.Lock()}

    def _get_account(self, acc_id: str):
        with self._lock:
            if acc_id not in self._accounts:
                raise ValueError("Account not found")
            return self._accounts[acc_id]

    def deposit(self, acc_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        account = self._get_account(acc_id)
        with account['lock']:
            account['balance'] += amount

    def withdraw(self, acc_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        account = self._get_account(acc_id)
        with account['lock']:
            if account['balance'] < amount:
                raise ValueError("Insufficient funds")
            account['balance'] -= amount

    def balance(self, acc_id: str) -> float:
        account = self._get_account(acc_id)
        with account['lock']:
            return account['balance']

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if from_id == to_id:
            return

        from_acc = self._get_account(from_id)
        to_acc = self._get_account(to_id)

        # Lock accounts in a consistent order to prevent deadlocks
        lock1_id, lock2_id = sorted((from_id, to_id))
        
        lock1 = self._accounts[lock1_id]['lock']
        lock2 = self._accounts[lock2_id]['lock']

        with lock1:
            with lock2:
                if from_acc['balance'] < amount:
                    raise ValueError("Insufficient funds")
                from_acc['balance'] -= amount
                to_acc['balance'] += amount
