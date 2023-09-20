from sage.all import SR, sqrt, matrix, vector

from utils_sage import Id, X, Y, Z
from chapter_8_sage import p, g, affine, toPauli


def test_toPauli():
    assert toPauli(Id) == [1, 0, 0, 0]
    assert toPauli(X)  == [0, 1, 0, 0]
    assert toPauli(Y)  == [0, 0, 1, 0]
    assert toPauli(Z)  == [0, 0, 0, 1]

    assert toPauli(X+2*Y+3*Z) == [0, 1, 2, 3]


def test_affine_bitflip():
    E0 = sqrt(p) * Id
    E1 = sqrt(1-p) * X

    M, c = affine(*[toPauli(E) for E in [E0, E1]])

    assert M == matrix.diagonal([1, 2*p-1, 2*p-1])
    assert c == vector([0, 0, 0])


def test_affine_amplitude_damping():
    E0 = matrix.diagonal([1, sqrt(1-g)])
    E1 = matrix([[0, sqrt(g)], [0, 0]])

    M, c = affine(*[toPauli(E) for E in [E0, E1]])
    M = M.expand()

    assert M == matrix.diagonal([sqrt(1-g), sqrt(1-g), 1-g])
    assert c == vector([0, 0, g])
