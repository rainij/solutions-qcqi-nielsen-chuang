from sage.all import i

from chapter_7_sage import x, p, a, ad

def test_position_and_momentum_operator():
    assert x*p - p*x == i
