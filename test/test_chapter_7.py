from sage.all import i

from chapter_7_sage import x, dx, p, a, ad

def test_position_momentum_ladder_operator():
    assert p == -i*dx
    assert x*p - p*x == i
    assert a*ad - ad*a == 1
