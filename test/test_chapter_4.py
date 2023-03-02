import pytest

from sympy import Matrix, I

from chapter_4 import tprod, make_CU, make_CnU, make_twolevel, make_onelevel, \
    Id, P0, P1, \
    X, Y, Z, S, \
    CX, CY, CZ, Toff


@pytest.mark.parametrize("args,prod", [
    ([P0, Id], Matrix([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]])),
    ([P1, Id], Matrix([[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])),
    ([X, Z], Matrix([[0,  0, 1,  0],
                     [0,  0, 0, -1],
                     [1,  0, 0,  0],
                     [0, -1, 0,  0]])),
    ([Z, X, S], Matrix([[0, 0, 1, 0,  0,  0,  0,  0],
                        [0, 0, 0, I,  0,  0,  0,  0],
                        [1, 0, 0, 0,  0,  0,  0,  0],
                        [0, I, 0, 0,  0,  0,  0,  0],
                        [0, 0, 0, 0,  0,  0, -1,  0],
                        [0, 0, 0, 0,  0,  0,  0, -I],
                        [0, 0, 0, 0, -1,  0,  0,  0],
                        [0, 0, 0, 0,  0, -I,  0,  0]])),
])
def test_tprod(args, prod):
    assert tprod(*args) == prod


@pytest.mark.parametrize("n,c,t,U,CU", [
    (2, 0, 1, X, CX),
    (2, 0, 1, Y, CY),
    (2, 0, 1, Z, CZ),
])
def test_make_CU(n, c, t, U, CU):
    assert make_CU(n, c, t, U) == CU


@pytest.mark.parametrize("n,cs,t,U,CU", [
    [3, [0, 1], 2, X, Toff],
])
def test_make_CnU(n, cs, t, U, CU):
    assert make_CnU(n, cs, t, U) == CU


@pytest.mark.parametrize("dim,indices,row,M", [
    (4, [1, 0], [3, 4], Matrix([[-4, 3, 0, 0],
                                [ 3, 4, 0, 0],
                                [ 0, 0, 5, 0],
                                [ 0, 0, 0, 5]]) / 5),
    (4, [2,1], [3, 4*I], Matrix([[5,   0,   0, 0],
                                 [0, 4*I,   3, 0],
                                 [0,   3, 4*I, 0],
                                 [0,   0,   0, 5]]) / 5),
])
def test_make_twolevel(dim, indices, row, M):
    assert make_twolevel(dim, indices, row) == M


@pytest.mark.parametrize("dim,index,factor,M", [
    (3, 1, 2, Matrix([[1, 0, 0],
                      [0, 2, 0],
                      [0, 0, 1]])),
])
def test_make_onelevel(dim, index, factor, M):
    assert make_onelevel(dim, index, factor) == M
