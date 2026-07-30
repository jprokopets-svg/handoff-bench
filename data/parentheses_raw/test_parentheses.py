from parentheses import *

import pytest


def test_generate_parentheses_1():
    assert sorted(generate_parentheses(1)) == sorted(['()'])

def test_generate_parentheses_2():
    assert sorted(generate_parentheses(2)) == sorted(['()()', '(())'])

def test_generate_parentheses_3_length():
    assert len(generate_parentheses(3)) == 5

def test_generate_parentheses_3():
    assert sorted(generate_parentheses(3)) == sorted(['((()))','(()())','(())()','()(())','()()()'])
