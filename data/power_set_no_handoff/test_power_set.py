from power_set import *

import pytest


assert sorted(power_set([1])) == sorted([[], [1]])

assert sorted(power_set([1,2])) == sorted([[], [1], [2], [1,2]])

assert len(power_set([1,2,3])) == 8