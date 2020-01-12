import pytest
from jokettt.board import *

def test_default_constructor():
    brd = Board('o', 'x')
    assert brd.is_empty()
