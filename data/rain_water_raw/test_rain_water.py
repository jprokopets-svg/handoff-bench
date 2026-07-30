from rain_water import *

import pytest


def test_trap_case1():
    assert trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6

def test_trap_case2():
    assert trap([4,2,0,3,2,5]) == 9

def test_trap_case3():
    assert trap([1,0,1]) == 1
