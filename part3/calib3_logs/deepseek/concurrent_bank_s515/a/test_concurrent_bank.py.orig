from concurrent_bank import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 100.0); b.deposit('b', 50.0); assert b.balance('a') == 100.0 and b.balance('b') == 50.0

b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 100.0); b.transfer('a', 'b', 30.0); assert b.balance('a') == 70.0 and b.balance('b') == 30.0

b = Bank(); b.create_account('a'); b.deposit('a', 10.0); assert _raises(lambda: b.withdraw('a', 20.0)); assert b.balance('a') == 10.0

b = Bank(); b.create_account('a'); assert _raises(lambda: b.deposit('a', 0.0))

b = Bank(); b.create_account('a'); assert _raises(lambda: b.deposit('a', -5.0))

b = Bank(); assert _raises(lambda: b.deposit('nope', 5.0))

b = Bank(); assert _raises(lambda: b.balance('nope'))

b = Bank(); b.create_account('a'); assert _raises(lambda: b.create_account('a'))

b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 10.0); assert _raises(lambda: b.transfer('a', 'b', 11.0)); assert b.balance('a') == 10.0 and b.balance('b') == 0.0

b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 10.0); assert _raises(lambda: b.transfer('a', 'zz', 1.0))

import threading

import sys; sys.setswitchinterval(1e-7)

b = Bank()
b.create_account('a0'); b.deposit('a0', 100000.0)
b.create_account('a1'); b.deposit('a1', 100000.0)
start = threading.Barrier(16)
errors = []
def worker(i):
    try:
        start.wait()
        f, t = ('a0', 'a1') if i % 2 == 0 else ('a1', 'a0')
        for _ in range(3000):
            b.transfer(f, t, 1.0)
    except Exception as e:
        errors.append(e)
threads = [threading.Thread(target=worker, args=(i,)) for i in range(16)]
for t in threads: t.start()
for t in threads: t.join()
assert not errors
assert b.balance('a0') == 100000.0 and b.balance('a1') == 100000.0
assert b.balance('a0') >= 0.0 and b.balance('a1') >= 0.0