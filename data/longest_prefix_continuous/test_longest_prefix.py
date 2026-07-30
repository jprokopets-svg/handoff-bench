from longest_prefix import *

import pytest


def test_flower_flow_flight():
    assert longest_common_prefix(['flower','flow','flight']) == 'fl'

def test_dog_racecar_car():
    assert longest_common_prefix(['dog','racecar','car']) == ''

def test_empty_string():
    assert longest_common_prefix(['']) == ''

def test_single_char():
    assert longest_common_prefix(['a']) == 'a'

def test_identical_strings():
    assert longest_common_prefix(['abc','abc','abc']) == 'abc'

def test_interspecies():
    assert longest_common_prefix(['interspecies','interstellar','interstate']) == 'inters'
