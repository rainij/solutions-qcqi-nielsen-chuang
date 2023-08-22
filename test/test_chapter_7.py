from sage.all import i, pi, matrix, sqrt

from chapter_7_sage import x, dx, p, a, ad, B, Pl, Dn, lambda_nl


def test_position_momentum_ladder_operator():
    assert p == -i*dx
    assert x*p - p*x == i
    assert a*ad - ad*a == 1


def test_beamsplitter():
    assert B.H * B == matrix.identity(2), "Should be orthogonal"
    assert B.subs(theta=pi/4) == matrix([[1, -1], [1, 1]]) / sqrt(2), \
        "Should be parameterized by theta in the right way"


def test_exercise_716():
    for l in range(6):
        for n in range(l+1):
            q = Dn(Pl(l), n) - lambda_nl(n, l)*Pl(l)
            assert q == 0
