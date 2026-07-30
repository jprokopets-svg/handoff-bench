from parentheses import generate_parentheses
import pytest


def test_generate_parentheses_n1():
    assert sorted(generate_parentheses(1)) == sorted(['()'])


def test_generate_parentheses_n2():
    assert sorted(generate_parentheses(2)) == sorted(['()()', '(())'])


def test_generate_parentheses_n3_length():
    assert len(generate_parentheses(3)) == 5


def test_generate_parentheses_n3():
    assert sorted(generate_parentheses(3)) == sorted(['((()))','(()())','(())()','()(())','()()()'])
