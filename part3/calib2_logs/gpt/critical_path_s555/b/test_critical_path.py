from critical_path import *


def _valid(durations, deps, dur, path):
    if abs(dur - sum(durations[t] for t in path)) > 1e-9:
        return False
    pos = {t: i for i, t in enumerate(path)}
    for a, b in deps:
        if a in pos and b in pos and pos[a] > pos[b]:
            return False
    return True

d, durs = critical_path({}, []); assert d == 0.0 and durs == []

d, p = critical_path({7: 3.5}, []); assert d == 3.5 and p == [7]

d, p = critical_path({1: 3, 2: 2, 3: 4}, []); assert d == 4.0 and _valid({1: 3, 2: 2, 3: 4}, [], d, p)

dur = {1: 2, 2: 4, 3: 3, 4: 6, 5: 2, 6: 1}
deps = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (3, 6), (5, 6)]
d, p = critical_path(dur, deps); assert d == 15.0 and _valid(dur, deps, d, p)

dur = {1: 5, 2: 7}; d, p = critical_path(dur, []); assert d == 7.0 and _valid(dur, [], d, p)

dur = {1: 1, 2: 1}
def _cyc():
    return critical_path(dur, [(1, 2), (2, 1)])
try:
    _cyc(); assert False
except ValueError:
    pass

dur = {1: 1, 2: 1, 3: 1}
d, p = critical_path(dur, [(1, 2), (2, 3)]); assert d == 3.0 and _valid(dur, [(1, 2), (2, 3)], d, p)

dur = {1: 2, 2: 5, 3: 1, 4: 2}
d, p = critical_path(dur, [(1, 3), (2, 3), (3, 4)]); assert d == 8.0 and _valid(dur, [(1, 3), (2, 3), (3, 4)], d, p)