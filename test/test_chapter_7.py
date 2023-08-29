from sage.all import i, pi, matrix, sqrt, SR

from chapter_7_sage import x, dx, p, a, ad, B, Pl, Dn, lambda_nl, column_normalized, restrict


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


def test_column_normalized():
    # M is implicitly over the integer ring:
    M = matrix([
        [3, 0, 0],
        [0, 1, 4],
        [0, 1, 3],
    ])

    Q = column_normalized(M)

    # The result is always over the symbolic ring (SR)
    Q_expected = matrix(SR, [
        [1, 0, 0],
        [0, 1/sqrt(2), 4/5],
        [0, 1/sqrt(2), 3/5],
    ])

    assert Q == Q_expected


def test_restrict():
    A = matrix([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ])

    M = matrix([
        [0, 1, 0],
        [1, 0, 0],
    ])

    A1 = restrict(A, M)

    A1_expected = matrix([
        [5, 4],
        [2, 1],
    ])

    assert A1 == A1_expected
