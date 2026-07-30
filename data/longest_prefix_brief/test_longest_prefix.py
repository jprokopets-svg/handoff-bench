from longest_prefix import longest_common_prefix
import pytest


def test_basic_case():
    assert longest_common_prefix(['flower','flow','flight']) == 'fl'


def test_no_common_prefix():
    assert longest_common_prefix(['dog','racecar','car']) == ''


def test_single_empty_string():
    assert longest_common_prefix(['']) == ''


def test_single_string():
    assert longest_common_prefix(['a']) == 'a'


def test_all_identical():
    assert longest_common_prefix(['abc','abc','abc']) == 'abc'


def test_long_common_prefix():
    assert longest_common_prefix(['interspecies','interstellar','interstate']) == 'inters'
