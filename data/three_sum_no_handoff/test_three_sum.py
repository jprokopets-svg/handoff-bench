from three_sum import *

import pytest


assert three_sum([-1,0,1,2,-1,-4]) == [[-1,-1,2],[-1,0,1]]

assert three_sum([0,1,1]) == []

assert three_sum([0,0,0]) == [[0,0,0]]