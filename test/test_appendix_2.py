import pytest

from sympy import eye, Matrix, exp, I, pi, sqrt

from appendix_2 import U_std, s3_perm, s3_std, get_fourier_matrix, s3_triv, s3_sign
from chapter_4 import H, tprod


def test_exercise_A2_17():
    """Test that U_std converts permutation representation into standard representation."""
    assert U_std.H * U_std == eye(3)
    assert len(s3_perm) == len(s3_std) == 6

    for i in range(6):
        print(i)
        G = U_std.H * s3_perm[i] * U_std
        G.col_del(0)
        G.row_del(0)

        assert G == s3_std[i]


w3 = exp(2*pi*I/3)


@pytest.mark.parametrize("data", [
    # Trivial group {e}:
    {
        "representations": [[1]],
        "result": Matrix([[1]]),
    },
    # Cyclic group of order 3 (standard fourier trafo)
    {
        # NOTE: The list of representations already looks like the matrix (up to factor).
        "representations": [
            [1, 1, 1],
            [1, w3, w3**2],
            [1, w3**2, w3**4],
        ],
        "result": Matrix([[w3**(i*j) / sqrt(3) for j in range(3)] for i in range(3)]),
    },
    # S_3 (exercise A2.24)
    {
        "representations": [s3_triv, s3_sign, s3_std],
        "result": Matrix([
            [sqrt(6)/6,  sqrt(6)/6,  sqrt(6)/6,  sqrt(6)/6,  sqrt(6)/6,  sqrt(6)/6],
            [sqrt(6)/6,  sqrt(6)/6,  sqrt(6)/6, -sqrt(6)/6, -sqrt(6)/6, -sqrt(6)/6],
            [sqrt(3)/3, -sqrt(3)/6, -sqrt(3)/6, -sqrt(3)/3,  sqrt(3)/6,  sqrt(3)/6],
            [        0,       -1/2,        1/2,          0,       -1/2,        1/2],
            [        0,        1/2,       -1/2,          0,       -1/2,        1/2],
            [sqrt(3)/3, -sqrt(3)/6, -sqrt(3)/6,  sqrt(3)/3, -sqrt(3)/6, -sqrt(3)/6],
        ]),
    },
    # Z_2 = {0, 1} with addition mod 2 (Hadamard trafo H)
    {
        "representations": [[1, 1], [1, -1]],
        "result": H,
    },
    # Z_2 ⨁ Z_2 (Hadamard trafo H ⮾ H)
    {
        # The representations are obtained as follows: Take a set of positions and for
        # each element count the ones at these positions. Even yields +1, odd yields -1.
        # Order matters: it corresponds to the natural counting: 00, 01, 10, 11.
        "representations": [
            [+1, +1, +1, +1],  # pos = {}
            [+1, -1, +1, -1],  # pos = {0}
            [+1, +1, -1, -1],  # pos = {1}
            [+1, -1, -1, +1],  # pos = {0, 1}
        ],
        "result": tprod(H, H),
    },
    # Z_2 ⨁ Z_2 ⨁ Z_2 (Hadamard trafo H ⮾ H ⮾ H)
    {
        "representations": [
            [(-1)**((i & j).bit_count()) for i in range(8)] \
            for j in range(8)
        ],
        "result": tprod(H, H, H),
    },
])
def test_get_fourier_matrix(data):
    assert get_fourier_matrix(data["representations"]) == data["result"]
