import itertools

import pytest
from sympy import Matrix

from chapter_2 import ptrace, trace


def make_range_matrix(n: int) -> Matrix:
    """Make [0,1,...,n**2-1] into an nxn matrix."""
    return Matrix([[n*i + j for j in range(n)] for i in range(n)])


A = make_range_matrix(4)
B = make_range_matrix(8)


@pytest.mark.parametrize("M,tr_M", [
    (A, 30),
    (B, 252),
])
def test_trace(M, tr_M):
    assert trace(M) == tr_M


@pytest.mark.parametrize("M,bit_positions,tr_M", [
    (A, [0], Matrix([[5, 9], [21, 25]])),
    (A, [1], Matrix([[10, 12], [18, 20]])),
    (A, [0, 1], Matrix([[30]])),
    (A, [1, 0], Matrix([[30]])),
    (B, [0], Matrix([[9, 13, 17, 21],
                     [41, 45, 49, 53],
                     [73, 77, 81, 85],
                     [105, 109, 113, 117]])),
    (B, [1], Matrix([[18, 20, 26, 28],
                     [34, 36, 42, 44],
                     [82, 84, 90, 92],
                     [98, 100, 106, 108]])),
    (B, [2], Matrix([[36, 38, 40, 42],
                     [52, 54, 56, 58],
                     [68, 70, 72, 74],
                     [84, 86, 88, 90]])),
    (B, [0, 1], Matrix([[54, 70], [182, 198]])),
    (B, [1, 0], Matrix([[54, 70], [182, 198]])),
    (B, [0, 2], Matrix([[90, 98], [154, 162]])),
    (B, [2, 0], Matrix([[90, 98], [154, 162]])),
    (B, [1, 2], Matrix([[108, 112], [140, 144]])),
    (B, [2, 1], Matrix([[108, 112], [140, 144]])),
    (B, [0, 1, 2], Matrix([[252]])),
    (B, [2, 0, 1], Matrix([[252]])),
    (B, [1, 2, 0], Matrix([[252]])),
    (B, [1, 0, 2], Matrix([[252]])),
    (B, [2, 1, 0], Matrix([[252]])),
    (B, [0, 2, 1], Matrix([[252]])),
], ids=itertools.count())
def test_ptrace(M, bit_positions, tr_M):
    assert ptrace(M, bit_positions) == tr_M
